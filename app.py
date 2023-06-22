from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle
from db_api import DbApi
from kernel.model_runner import ModelRunner
from kernel.data_info import DataInfo

def create_app():
    app = Flask(__name__)
    db_api = DbApi()
    app.model_runner = ModelRunner(db_api)

    @app.route('/')
    def hello_world():  # put application's code here
        return render_template("index.html")

    @app.route('/model', methods=['POST'])
    def upload_model():
        """
        Загрузить предиктивную модель для факультета
        """

        faculty = request.args.get('faculty')
        if faculty is None:
            faculty = 'cs_b'
        model_pkl = request.files.get('model_miem_mag.cbm').read()
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

                    db_api.save_mark(student_id, names_2_ids[course_name], module, value)

        model_pkl = db_api.get_model(faculty)
        model = pickle.loads(model_pkl)


        model_pkl = pickle.dumps(model, protocol=pickle.HIGHEST_PROTOCOL)
        db_api.save_model(faculty, model_pkl)

        return render_template("index.html")

    @app.route('/prediction', methods=['GET'])
    def get_prediction():
        """
        Получить предсказание по студенту
        """
        dto_in = DataInfo(
            model_category='miem_mag'
        )
        # student_id = request.args.get('st_type')

        result = app.model_runner.get_prediction(dto_in)

        return result

    return app
