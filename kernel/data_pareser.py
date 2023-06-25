from db_api import DBOrm
import pandas as pd
from db_api import Faculty, Subject, Student, Degree, Mark

class DataProcessor:

    def __init__(self, db_orm: DBOrm):
        self.db_orm = db_orm

    def parse_and_load_student_info(self, data_csv, sep):
        df = pd.read_csv(data_csv, sep=sep)

        return self.db_orm.add_student_info(df)


    def parce_and_load_subject_info(self, data_csv, sep, prefix):
        subjects = pd.read_csv(data_csv, sep=sep)

        existed_subject_key = self.db_orm.get_all_exist_subject()

        subjects_for_insert = [Subject(
            subject_id=f'{prefix}_{row["ID"]}',
            subject_name=row['Subject']
        ) for i, row in subjects.iterrows() if f'{prefix}_{row["ID"]}' not in existed_subject_key]

        existed_subject = [
            row['ID']
            for i, row in subjects.iterrows() if f'{prefix}_{row["ID"]}' in existed_subject_key
        ]

        self.db_orm.add_subjects(subjects_for_insert)

        return (len(subjects_for_insert), list(existed_subject))
