from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle
from db_api import DbApi


class Model:
    def fit(self, x):
        pass

    def predict(self, x):
        pass


app = Flask(__name__)
db_api = DbApi()


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/model', methods=['POST'])
def upload_model():
    """
    Загрузить предиктивную модель для факультета
    """

    faculty = request.args.get('faculty')
    if faculty is None:  # TODO: передавать аргумент
        faculty = 'cs_b'
    model_pkl = request.files.get('model').read()
    # print(model_pkl)

    db_api.save_model(faculty, model_pkl)

    return render_template("index.html")


@app.route('/data', methods=['POST'])
def upload_data():
    """
    Загрузить csv-таблицу
    """

    faculty = request.args.get('faculty')
    data_csv = request.files.get('data')
    df = pd.read_csv(data_csv)

    courses_names = df.columns.values[2:]
    names_2_ids = db_api.get_courses_ids_by_names(tuple(courses_names))

    for i, row in df.iterrows():
        student_id = int(row.get('id'))
        module = int(row.get('module'))
        for j in range(len(courses_names)):
            course_name = courses_names[j]
            value = row.get(course_name)
            if not np.isnan(value):
                # TODO: оптимизировать
                db_api.save_mark(student_id, names_2_ids[course_name], module, value)

    model_pkl = db_api.get_model(faculty)
    model = pickle.loads(model_pkl)
    # TODO: дообучить/переобучить модель

    model_pkl = pickle.dumps(model, protocol=pickle.HIGHEST_PROTOCOL)
    db_api.save_model(faculty, model_pkl)

    return render_template("index.html")


@app.route('/prediction', methods=['GET'])
def get_prediction():
    """
    Получить предсказание по студенту
    """

    student_id = request.args.get('student_id')
    student = db_api.get_student(student_id)
    model_pkl = bytes(db_api.get_model(student['faculty']))
    # print(model_pkl)
    # print(type(model_pkl))
    # TODO: загружать модель
    model = pickle.loads(model_pkl)

    # sql -> Dataframe -> model.predict()
    db_api.get_student_marks(student_id)

    return render_template("index.html")


if __name__ == '__main__':
    app.run()
