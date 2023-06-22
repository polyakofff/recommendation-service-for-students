import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, SmallInteger

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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
    program_id = Column(Integer, ForeignKey('program.program_id'), nullable=True)

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
            return prefix_creator(self.degrees_info.get(student.degree_id), self.faculcy_info.get(student.faculty_id))


class DbApi:
    def __init__(self):
        host = 'localhost'
        try:
            self.connection = psycopg2.connect(
                host=host,
                dbname='postgres',
                user='postgres',
                password='postgres',
            )
            self.connection.autocommit = True
            print(f'Connection to db ({host}) is successful')
        except:
            print(f'Connection to db ({host}) failed')

    def get_student(self, student_id):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            select *
            from student
            where id = %s
            ''', student_id)

            r = cursor.fetchone()
            if r is None:
                raise Exception(f'Не найдено записей в бд (pk={student_id})')
            return {'id': r[0], 'name': r[1], 'faculty': r[2]}

    def get_courses_ids_by_names(self, names):
        if len(names) == 0:
            return {}
        res = {}
        with self.connection.cursor() as cursor:
            cursor.execute('''
            select * 
            from course 
            where name in %s
            ''', (names,))

            rs = cursor.fetchall()
            for r in rs:
                res[r[1]] = r[0]

        return res

    def save_mark(self, student_id, course_id, module, value):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            insert into mark(student_id, course_id, module, value) 
            values (%s, %s, %s, %s)
            ''', (student_id, course_id, module, value))

        return 1

    def get_student_marks(self, student_id):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            select m.value
            from course c
                left join (
                    select m.*
                    from mark m
                        left join mark m2 on m.student_id = m2.student_id
                                         and m.course_id = m2.course_id
                                         and m.module < m2.module
                    where m2 is null
                ) m on c.id = m.course_id
            where m is null or m.student_id = %s
            order by c.id
            ''', (student_id,))

            rs = cursor.fetchall()
            print(type(rs))
            print(rs)



