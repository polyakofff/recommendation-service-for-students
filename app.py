from flask import Flask, render_template, request, abort
import pandas as pd
from db_api import DBOrm
from kernel.model_runner import ModelRunner
from constant.model_categories import PREFIX_INFO
from kernel.data_pareser import DataProcessor

def create_app():
    app = Flask(__name__)
    db_orm = DBOrm()
    app.model_runner = ModelRunner(db_orm)
    app.data_processor = DataProcessor(db_orm)

    @app.route('/')
    def hello_world():
        return render_template("index.html")

    @app.errorhandler(403)
    def internal_server_error(e):
        return 'prefix не из списка валидных, для получение валидных префиксов вызовите ручку get_prefix', 403

    @app.route('/set_date_subject', methods=['POST'])
    def upload_subject_data():
        prefix = request.args.get('prefix')
        sep = request.args.get('sep')
        if prefix not in PREFIX_INFO:
            abort(403)
        data_csv = request.files.get('data')
        try:
            subject_count, exist_subject = app.data_processor.parce_and_load_subject_info(data_csv, sep, prefix)
        except Exception as e:
            return {
                'succes': False,
                'error': str(e)
            }

        return {
            'subject_count_insert': subject_count,
            'subject_count_not_insert': len(exist_subject),
            'exist_subjects': exist_subject
        }

    @app.route('/set_data_student', methods=['POST'])
    def upload_student_data():
        data_csv = request.files.get('data')
        sep = request.args.get('sep')
        count_added_student, all_st, prefix, mark_for_insert, col_with_error = app.data_processor.parse_and_load_student_info(data_csv, sep)
        return {
            'count_added_student': count_added_student,
            'count_unique_student': all_st,
            'type': prefix,
            'count_mark': mark_for_insert,
            'count_col_with_error': len(list(col_with_error)),
            'col_with_error': list(col_with_error)
        }

    @app.route('/get_prefix', methods=['GET'])
    def get_prefix_info():
        return PREFIX_INFO

    @app.route('/prediction', methods=['GET'])
    def get_prediction():
        request_data = request.get_json()
        student_id = request_data['student_id']
        predict, prefix = app.model_runner.get_prediction(student_id)
        return {
            'type': prefix,
            'predict': predict
        }

    @app.route('/help', methods=['GET'])
    def help_method():
        return [app.db_orm.degrees_info, app.db_orm.faculcy_info]

    return app
