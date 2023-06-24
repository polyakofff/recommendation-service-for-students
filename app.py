from flask import Flask, render_template, request, abort
import pandas as pd
from db_api import DBOrm
from kernel.model_runner import ModelRunner
from constant.model_categories import PREFIX_INFO


def create_app():
    app = Flask(__name__)
    app.db_orm = DBOrm()
    app.model_runner = ModelRunner()

    @app.route('/')
    def hello_world():  # put application's code here
        return render_template("index.html")

    @app.errorhandler(403)
    def internal_server_error(e):
        return 'prefix не из списка валидных, для получение валидных префиксов вызовите ручку get_prefix', 403

    @app.route('/date_subject', methods=['POST'])
    def upload_subject_data():
        prefix = request.args.get('prefix')
        sep = request.args.get('sep')
        if prefix not in PREFIX_INFO:
            abort(403)
        data_csv = request.files.get('data')
        df = pd.read_csv(data_csv, sep=sep)
        subject_count, exist_subject = app.db_orm.add_subjects(prefix, df)
        return {
            'success': True,
            'subject_count_insert': subject_count,
            'subject_count_not_insert': len(exist_subject),
            'exist_subjects': exist_subject
        }

    @app.route('/data_student', methods=['POST'])
    def upload_student_data():
        data_csv = request.files.get('data')
        sep = request.args.get('sep')
        df = pd.read_csv(data_csv, sep=sep)
        count_added_student, all_st, prefix, mark_for_insert, col_with_error = app.db_orm.add_student_info(df)
        return {
            'success': True,
            'count_added_student': count_added_student,
            'all_identify_st': all_st,
            'type': prefix,
            'mark_for_insert_count': mark_for_insert,
            'count_col_with_error': len(list(col_with_error)),
            'col_lis': list(col_with_error)
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
        df_features, prefix = app.db_orm.get_features_for_student(student_id)

        predict = app.model_runner.get_prediction(df_features, prefix)

        return {
            'success': True,
            'module_type': prefix,
            'predict': predict
        }

    @app.route('/help', methods=['GET'])
    def help_method():
        return [app.db_orm.degrees_info, app.db_orm.faculcy_info]

    return app
