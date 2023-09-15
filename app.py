from flask import Flask, render_template, request
import pandas as pd
from db_api import DbApi
from model_manager import ModelManager


app = Flask(__name__)
db_api = DbApi()
model_manager = ModelManager()


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/data', methods=['POST'])
def upload_data():
    """
    Загрузить csv-таблицу с оценками в формате:
    ID,Факультет,Образовательная программа,Уровень обучения,Курс,Модуль,Предмет 1,Предмет 2,...
    ...

    Оценки для конкретного факультета на конкретной ступени образования (бакалавриат/магистратура)
    """

    faculty = request.args.get('faculty')
    degree = request.args.get('degree')
    data_csv = request.files.get('data')

    df = pd.read_csv(data_csv)

    subjects = df.columns.drop(['ID', 'Факультет', 'Образовательная программа', 'Уровень обучения', 'Курс', 'Модуль']).values
    subjects_present = db_api.get_all_subjects_by_fac_and_deg(faculty, degree)
    subjects_dif = list(set(subjects) - set([s[1] for s in subjects_present]))
    subjects_to_add = [(s, faculty, degree) for s in subjects_dif]
    subjects_added = db_api.save_subjects_by_fac_and_deg(subjects_to_add)
    print(f'subjects added: {subjects_added}')
    subjects_name_to_id = {s[1]: s[0] for s in (subjects_present + subjects_added)}

    student_ids = []
    marks = []
    for i, row in df.iterrows():
        student_id = int(row.get('ID'))
        student_ids.append(student_id)
        level = int(row.get('Курс'))
        module = int(row.get('Модуль'))
        module16 = (level - 1) * 4 + module
        for subject in subjects:
            subject_id = subjects_name_to_id[subject]
            value = row[subject]
            if not pd.isnull(value):
                marks.append((student_id, subject_id, module16, value))

    print(f'student ids: {student_ids}')
    db_api.save_students([(id, faculty, degree) for id in student_ids])
    print(f'marks: {marks}')
    db_api.save_marks(marks)

    return render_template("index.html")


@app.route('/prediction', methods=['GET'])
def get_prediction():
    """
    Получить предсказание по студенту
    """

    student_id = request.args.get('student_id')
    student = db_api.get_student(student_id)
    faculty = student[1]
    degree = student[2]

    # create dataframe
    subjects = db_api.get_all_subjects_by_fac_and_deg(faculty, degree)
    marks = db_api.get_student_marks(student_id) # subject,module,value

    marks_by_module = {}
    for m in marks:
        module = m[1]
        if module not in marks_by_module:
            marks_by_module[module] = []
        marks_by_module[module].append((m[0], m[2]))

    rows = []
    prev_module = 0
    for module in sorted(marks_by_module.keys()):
        while prev_module + 1 < module:
            prev_module += 1
            rows.append({'module': prev_module})
        row = {m[0]: m[1] for m in marks_by_module[module]}
        row['module'] = module
        rows.append(row)
        prev_module = module

    df = pd.DataFrame(rows, columns=['module'] + [s[1] for s in subjects])
    print(df)

    model = model_manager.get_model(faculty, degree)
    model.get_prediction(df)

    return render_template("index.html")


if __name__ == '__main__':
    app.run()
