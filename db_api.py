import psycopg2
from psycopg2 import sql

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

        self.faculties = self.get_all_faculties()
        self.degrees = self.get_all_degrees()

    def get_all_faculties(self):
        return self.get_all('faculty')

    def get_all_degrees(self):
        return self.get_all('degree')

    def get_all(self, table_name):
        with self.connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("select * from {t}")
                    .format(t=sql.Identifier(table_name)))
            return cursor.fetchall()

    def get_all_subjects_by_fac_and_deg(self, faculty, degree):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from subject where faculty = %s and degree = %s", [faculty, degree])
            return cursor.fetchall()

    def save_subjects_by_fac_and_deg(self, subjects):
        with self.connection.cursor() as cursor:
            values = ','.join(cursor.mogrify("(%s, %s, %s)", s).decode('utf-8') for s in subjects)
            if len(values) == 0:
                return []
            cursor.execute("insert into subject (name, faculty, degree) values " + values + " returning *")
            return cursor.fetchall()

    def save_students(self, students):
        with self.connection.cursor() as cursor:
            values = ','.join(cursor.mogrify("(%s, %s, %s)", s).decode('utf-8') for s in students)
            if len(values) == 0:
                return []
            cursor.execute("insert into student (id, faculty, degree) values " + values + " on conflict do nothing")

    def save_marks(self, marks):
        with self.connection.cursor() as cursor:
            values = ','.join(cursor.mogrify("(%s, %s, %s, %s)", m).decode('utf-8') for m in marks)
            if len(values) == 0:
                return []
            cursor.execute("insert into mark (student_id, subject_id, module, value) values " + values +
                           " on conflict (student_id, subject_id, module) do update set value = EXCLUDED.value")

    def get_student(self, id):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from student where id = %s", id)
            return cursor.fetchone()

    def get_student_marks(self, id):
        with self.connection.cursor() as cursor:
            cursor.execute("select s.name, m.module, m.value "
                           "from mark m "
                           "    join subject s on m.subject_id = s.id "
                           "where m.student_id = %s", [id])
            return cursor.fetchall()
