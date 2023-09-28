from flask import Flask, render_template, request, abort
from db_api import DbApi
from data_transformer import DataTransformer
from model_manager import ModelManager


app = Flask(__name__)
db_api = DbApi()
data_transformer = DataTransformer(db_api)
model_manager = ModelManager()


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")

@app.errorhandler(400)
def bad_request(e):
    return e, 400

@app.route('/subjects', methods=['POST'])
def upload_subjects():
    """
    Загрузить csv-таблицу с предметами в формате:
    ID,Subject
    ...

    """

    faculty = request.args.get('faculty')
    degree = request.args.get('degree')
    if faculty is None or degree is None:
        abort(400, 'faculty or/and degree not set')
    data_csv = request.files.get('data')

    subjects_added = data_transformer.save_subjects(faculty, degree, data_csv)

    return {
               "subjects added: ": subjects_added
           }, 200


@app.route('/data', methods=['POST'])
def upload_data():
    """
    Загрузить csv-таблицу с оценками в формате:
    ID,Факультет,Образовательная программа,Уровень обучения,Курс,Модуль,Предмет 1,Предмет 2,...
    ...

    """

    faculty = request.args.get('faculty')
    degree = request.args.get('degree')
    if faculty is None or degree is None:
        abort(400, 'faculty or/and degree not set')
    data_csv = request.files.get('data')

    marks_added_or_updated = data_transformer.save_marks(faculty, degree, data_csv)

    return {
               "marks added or updated": marks_added_or_updated
           }, 200


@app.route('/prediction', methods=['GET'])
def get_prediction():
    """
    Получить предсказание по студенту
    """

    faculty = request.args.get('faculty')
    degree = request.args.get('degree')
    if faculty is None or degree is None:
        abort(400, 'faculty or/and degree not set')
    id = int(request.args.get('id'))

    student = db_api.get_student_by_fac_and_deg(id, faculty, degree)
    if student is None:
        abort(400, f'student with id={id} not found')

    # create dataframe
    df, subjects_id_2_name = data_transformer.build_dataframe(student[0], faculty, degree)
    print(df)

    model = model_manager.get_model(faculty, degree)
    pred = model.get_prediction(df)
    print(pred)

    return {
               "probability of exclusion": pred[1]
           }, 200


@app.route('/recommend', methods=['GET'])
def recommend():
    """
    Получить рекомендации по студенту
    """

    faculty = request.args.get('faculty')
    degree = request.args.get('degree')
    if faculty is None or degree is None:
        abort(400, 'faculty or/and degree not set')
    id = int(request.args.get('id'))
    n = int(request.args.get('n'))

    student = db_api.get_student_by_fac_and_deg(id, faculty, degree)
    if student is None:
        abort(400, f'student with id={id} not found')

    # create dataframe
    df, subjects_id_2_name = data_transformer.build_dataframe(student[0], faculty, degree)
    print(df)

    model = model_manager.get_model(faculty, degree)
    recs = model.recommend(df, subjects_id_2_name, n)
    print(recs)

    return {
               "recommendations": recs
           }, 200


if __name__ == '__main__':
    app.run()
