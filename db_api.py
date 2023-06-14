import psycopg2

class DbApi:

    def save_mark(self, student_id, course_id, module, value):
        with self.connection.cursor() as cursor:
            cursor.execute('INSERT INTO mark(student_id, course_id, module, value) VALUES (%s, %s, %s, %s)',
                           (student_id, course_id, module, value))

        return 1

    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host='localhost:5432',
                dbname='postgres',
                user='postgres',
                password='postgres',
            )
            self.connection.autocommit = True
        except:
            print(f'Can\' connect to database')


