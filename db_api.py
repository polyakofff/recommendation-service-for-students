import psycopg2
from models.model_category import create_prefix


class DbApi:

    def __init__(self):
        host = 'localhost'
        try:
            self.connection = psycopg2.connect(
                host=host,
                dbname='postgres',
                user='postgres',
                password='postgres',
            )
            self.connection.autocommit = True
            print(f'Connection to db ({host}) is successful')
        except:
            print(f'Connection to db ({host}) failed')

    def get_subjects_by_fac_and_deg(self, faculty, degree):
        prefix = create_prefix(faculty, degree)
        return self.get_subjects_by_prefix(prefix)

    def get_subjects_by_prefix(self, prefix):
        with self.connection.cursor() as cursor:
            cursor.execute("select id, name from subject where id like %s", [prefix + '%'])
            return cursor.fetchall()

    def save_subjects(self, subjects):
        with self.connection.cursor() as cursor:
            values = ','.join(cursor.mogrify("(%s, %s)", s).decode('utf-8') for s in subjects)
            if len(values) == 0:
                return
            cursor.execute("insert into subject (id, name) values " + values)

    def save_students(self, students):
        with self.connection.cursor() as cursor:
            values = ','.join(cursor.mogrify("(%s)", (s,)).decode('utf-8') for s in students)
            if len(values) == 0:
                return
            cursor.execute("insert into student (id) values " + values + " on conflict do nothing")

    def save_marks(self, marks):
        with self.connection.cursor() as cursor:
            values = ','.join(cursor.mogrify("(%s, %s, %s, %s)", m).decode('utf-8') for m in marks)
            if len(values) == 0:
                return
            cursor.execute("insert into mark (student_id, subject_id, module, value) values " + values +
                           " on conflict (student_id, subject_id, module) do update set value = EXCLUDED.value")

    def get_student_by_fac_and_deg(self, id, faculty, degree):
        prefix = create_prefix(faculty, degree)
        id = prefix + '_' + str(id)
        with self.connection.cursor() as cursor:
            cursor.execute("select * from student where id = %s", [id])
            return cursor.fetchone()

    def get_student_marks(self, id):
        with self.connection.cursor() as cursor:
            cursor.execute("select m.subject_id, m.module, m.value "
                           "from mark m "
                           "where m.student_id = %s", [id])
            return cursor.fetchall()
