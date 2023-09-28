import pandas as pd
from models.model_category import create_prefix, PREFIX_MAP


class DataTransformer:

    def __init__(self, db_api):
        self.db_api = db_api

    def save_subjects(self, faculty, degree, data_csv):
        prefix = create_prefix(faculty, degree)
        if prefix not in PREFIX_MAP:
            raise ValueError(f'Non-existent prefix \'{prefix}\'')

        df = pd.read_csv(data_csv, sep=';')
        subjects_present = self.db_api.get_subjects_by_prefix(prefix)
        ids = set(s[0] for s in subjects_present)

        subjects_to_add = []
        for i, row in df.iterrows():
            id = prefix + '_' + row['ID']
            name = row['Subject']
            if id not in ids:
                subjects_to_add.append((id, name))

        self.db_api.save_subjects(subjects_to_add)

        return len(subjects_to_add)

    def save_marks(self, faculty, degree, data_csv):
        prefix = create_prefix(faculty, degree)
        if prefix not in PREFIX_MAP:
            raise ValueError(f'Non-existent prefix \'{prefix}\'')

        df = pd.read_csv(data_csv, sep=';')
        # remove duplicated columns
        df = df.loc[:, ~df.columns.str.replace("(\.\d+)$", "", regex=True).duplicated()]

        subjects = df.columns.drop(
            ['ID', 'Факультет', 'Образовательная программа', 'Уровень обучения', 'Курс', 'Модуль']).tolist()

        subjects_present = self.db_api.get_subjects_by_prefix(prefix)
        subjects_name_to_id = {s[1]: s[0] for s in subjects_present}

        student_ids = set()
        marks = []
        for i, row in df.iterrows():
            student_id = prefix + '_' + str(row['ID'])
            student_ids.add(student_id)
            level = row['Курс']
            module = row['Модуль']
            module16 = (level - 1) * 4 + module
            for subject in subjects:
                subject_id = subjects_name_to_id[subject]
                value = row[subject]
                if not pd.isnull(value):
                    marks.append((student_id, subject_id, module16, value))

        print(f'student ids: {student_ids}')
        self.db_api.save_students(student_ids)
        self.db_api.save_marks(marks)

        return len(marks)

    def build_dataframe(self, student_id, faculty, degree):
        prefix = create_prefix(faculty, degree)
        subjects = self.db_api.get_subjects_by_prefix(prefix)
        subjects_id_2_name = {s[0].split('_')[-1]: s[1] for s in subjects}
        subjects_ids_no_prefix = [s[0].split('_')[-1] for s in subjects]
        marks = self.db_api.get_student_marks(student_id)  # subject,module,value

        marks_by_module = {}
        for m in marks:
            module = m[1]
            if module not in marks_by_module:
                marks_by_module[module] = []
            subject_id_no_prefix = m[0].split('_')[-1]
            marks_by_module[module].append((subject_id_no_prefix, m[2]))

        rows = []
        prev_module = 0
        for module in sorted(marks_by_module.keys()):
            while prev_module + 1 < module:
                prev_module += 1
                rows.append({'Module': prev_module})
            row = {m[0]: m[1] for m in marks_by_module[module]}
            row['Module'] = module
            rows.append(row)
            prev_module = module

        df = pd.DataFrame(rows, columns=['Module'] + subjects_ids_no_prefix)
        return df, subjects_id_2_name
