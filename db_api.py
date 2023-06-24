import copy
from sqlalchemy import create_engine, Integer, String, \
    Column, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from constant.model_categories import prefix_creator

Base = declarative_base()


class Subject(Base):
    __tablename__ = 'subject'
    subject_id = Column(String(100), primary_key=True)
    subject_name = Column(String(100), nullable=False)


class Degree(Base):
    __tablename__ = 'degree'
    degree_id = Column(Integer(), primary_key=True)
    degree_name = Column(String(100), nullable=False)
    degree_tag = Column(String(100), nullable=False)


class Faculty(Base):
    __tablename__ = 'faculty'
    faculty_id = Column(Integer(), primary_key=True)
    faculty_name = Column(String(100), nullable=False)
    faculty_tag = Column(String(100), nullable=False)


class Program(Base):
    __tablename__ = 'program'
    program_id = Column(Integer(), primary_key=True)
    program_name = Column(String(100), nullable=False)


class Student(Base):
    __tablename__ = 'student'
    student_id = Column(Integer(), primary_key=True)
    faculty_id = Column(Integer, ForeignKey('faculty.faculty_id'))
    degree_id = Column(Integer, ForeignKey('degree.degree_id'))
    program_id = Column(Integer, ForeignKey('program.program_id'))


class Mark(Base):
    __tablename__ = 'mark'
    mark_id = Column(Integer(), primary_key=True, autoincrement=True)
    module = Column(Integer(), nullable=False)
    estimation = Column(Integer(), nullable=False)
    subject_id = Column(String(100), ForeignKey('subject.subject_id'), nullable=False)
    student_id = Column(Integer(), ForeignKey('student.student_id'), nullable=False)


class DBOrm:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/postgres")
        self.Session = sessionmaker(self.engine)
        self.upload_general_data()

    def upload_general_data(self):
        with self.Session() as session:
            self.degrees_info = {degree.degree_id: degree.degree_tag for degree in session.query(Degree).all()}
            self.faculcy_info = {faculcy.faculty_id: faculcy.faculty_tag for faculcy in session.query(Faculty).all()}

    def add_subjects(self, prefix: str, subjects):
        with self.Session() as session:
            existed_subject_key = {subject.subject_id for subject in session.query(Subject).all()}

        subjects_for_insert = [Subject(
            subject_id=f'{prefix}_{row["ID"]}',
            subject_name=row['Subject']
        ) for i, row in subjects.iterrows() if f'{prefix}_{row["ID"]}' not in existed_subject_key]

        existed_subject = [
            row['ID']
            for i, row in subjects.iterrows() if f'{prefix}_{row["ID"]}' in existed_subject_key
        ]

        with self.Session() as session:
            session.add_all(subjects_for_insert)
            session.commit()

        return (len(subjects_for_insert), list(existed_subject))

    def get_model_prefix_for_stident_id(self, student_id):
        with self.Session() as session:
            student = session.query(Student).get(student_id)
            if not student:
                return None
            prefix = prefix_creator(self.degrees_info.get(student.degree_id), self.faculcy_info.get(student.faculty_id))
        return prefix

    def get_features_for_student(self, student_id):
        prefix = self.get_model_prefix_for_stident_id(student_id)

        with self.Session() as session:
            features_column = [subject.subject_id for subject in
                               session.query(Subject).filter(Subject.subject_id.like(f"{prefix}%")).all()]
        dict_of_key = {col.split('_')[-1]: None for col in features_column}

        with self.Session() as session:
            marks_for_student = session.query(Mark).filter(Mark.student_id == student_id).all()

        modules = sorted(list(set([mark.module for mark in marks_for_student])))

        dict_for_data = {}

        for module in modules:
            value_dict = copy.deepcopy(dict_of_key)
            value_dict['Module'] = module
            dict_for_data[module] = value_dict

        for mark in marks_for_student:
            mark_key = mark.subject_id.split('_')[-1]
            dict_for_data[mark.module][mark_key] = mark.estimation

        if not dict_for_data:
            return None
        df_col = list(dict_of_key.keys()) + ['Module']

        dict_for_pf = {col: [] for col in df_col}

        for module, module_val in dict_for_data.items():
            for col, value in module_val.items():
                dict_for_pf[col].append(value)

        return pd.DataFrame(dict_for_pf), prefix

    def add_student_info(self, data):
        columns_withount_estimate = ['Курс', 'Уровень обучения', 'Образовательная программа', 'Факультет', 'ID',
                                     'Модуль']

        with self.Session() as session:
            degrees_id_by_name = {degree.degree_name: degree.degree_id for degree in session.query(Degree).all()}
            faculcy_id_by_name = {faculcy.faculty_name: faculcy.faculty_id for faculcy in session.query(Faculty).all()}

        count_added_student, all_st, prefix = self.add_students(data, degrees_id_by_name, faculcy_id_by_name)

        with self.Session() as session:
            subject_id_by_name = {
                subject.subject_name: subject.subject_id
                for subject in session.query(Subject).filter(Subject.subject_id.like(f"{prefix}%")).all()}

        mark_for_insert = []
        col_with_error = set()
        for i, row in data.iterrows():
            for col in data.columns:
                if col in columns_withount_estimate:
                    continue

                if pd.isna(row[col]):
                    continue

                if col not in subject_id_by_name:
                    normal_col_name = col[:-2]
                    if normal_col_name not in subject_id_by_name:
                        col_with_error.add(col)
                        continue
                else:
                    normal_col_name = col

                subject_id = subject_id_by_name[normal_col_name]
                estimate = row[col]
                module = row['Модуль'] + 4 * (row['Курс'] - 1)
                student_id = row['ID']

                mark_for_insert.append(Mark(
                    subject_id=subject_id,
                    estimation=estimate,
                    module=module,
                    student_id=student_id
                )
                )

        with self.Session() as session:
            session.add_all(mark_for_insert)
            session.commit()

        return count_added_student, all_st, prefix, len(mark_for_insert), col_with_error

    def add_students(self, data, degrees_id_by_name, faculcy_id_by_name):
        with self.Session() as session:
            process_st = set()
            students = []
            prefix = ''

            for i, row in data.iterrows():
                st = Student(
                    student_id=row['ID'],
                    faculty_id=faculcy_id_by_name[row['Факультет']],
                    degree_id=degrees_id_by_name[row['Уровень обучения']],
                )
                prefix = prefix_creator(self.degrees_info[st.degree_id], self.faculcy_info[st.faculty_id])
                if st.student_id in process_st:
                    continue

                process_st.add(st.student_id)
                students.append(st)

            student_ids = [student.student_id for student in students]
            existed_st = set()

            for id in student_ids:
                res = session.query(Student).get(id)
                if not res:
                    continue
                existed_st.add(res.student_id)

            st_for_add = [student for student in students if student.student_id not in existed_st]
            session.add_all(st_for_add)
            session.commit()
            return len(st_for_add), len(list(students)), prefix
