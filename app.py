from flask import Flask, render_template, request, abort
import numpy as np
import pandas as pd
import pickle
from db_api import DbApi, DBOrm
from kernel.model_runner import ModelRunner
from kernel.data_info import DataInfo
from constant.model_categories import PREFIX_INFO

def create_app():
    app = Flask(__name__)
    db_api = DbApi()
    app.db_orm = DBOrm()
    app.model_runner = ModelRunner(db_api)

    @app.route('/')
    def hello_world():  # put application's code here
        return render_template("index.html")

    @app.errorhandler(403)
    def internal_server_error(e):
        return 'prefix не из списка валидных, для получение валидных префиксов вызовите ручку get_prefix', 403

    @app.route('/date_subject', methods=['POST'])
    def upload_subject_data():
        prefix = request.args.get('prefix')
        if prefix not in PREFIX_INFO:
            abort(403)
        data_csv = request.files.get('data')
        df = pd.read_csv(data_csv)
        subject_count, exist_subject = app.db_orm.add_subjects(prefix, df)
        return {
            'success': True,
            'subject_count_insert': subject_count,
            'subject_count_not_insert': len(exist_subject),
            'exist_subjects': exist_subject
        }

    @app.route('/get_prefix', methods=['GET'])
    def get_prefix_info():
        return PREFIX_INFO

    @app.route('/prediction', methods=['GET'])
    def get_prediction():
        """
        Получить предсказание по студенту
        """
        request_data = request.get_json()
        #
        student_id = request_data['student_id']
        model_type = app.db_orm.get_model_prefix_for_stident_id(student_id)
        if not model_type:
            return {
                'success': False,
                'error': 'Такого пользователся не существует'
            }

        dto_in = DataInfo(
            model_category=model_type
        )

        result = app.model_runner.get_prediction(dto_in)

        return {
            'success': True
        }

    @app.route('/help', methods=['GET'])
    def help_method():
        return [app.db_orm.degrees_info, app.db_orm.faculcy_info]

    return app
