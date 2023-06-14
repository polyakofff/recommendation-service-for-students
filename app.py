from flask import Flask, render_template, request
import pandas as pd
from db_api import DbApi

app = Flask(__name__)
db_api = DbApi()


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/model', methods=['POST'])
def upload_model():

    pass


@app.route('/data', methods=['POST'])
def upload_data():
    f = request.files.get('file')
    df = pd.read_csv(f)

    courses = df.columns.values[2:]
    print(courses)
    for i, row in df.iterrows():
        student_id = row.get('student_id')
        module = row.get('module')
        for j in range(len(courses)):
            value = row.get(courses[j])
            db_api.save_mark(student_id, -1, module, value)


    return render_template("index.html")


@app.route('/prediction', methods=['GET'])
def get_prediction():

    pass


if __name__ == '__main__':
    app.run()
