import psycopg2


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

    def save_model(self, faculty, model):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            insert into faculty_model(faculty, model) 
            values (%s, %s)
            ''', (faculty, model))

    def get_model(self, faculty):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            select model
            from faculty_model
            where faculty = %s
            ''', (faculty,))

            r = cursor.fetchone()
            if r is None:
                raise Exception(f'Не найдено записей в бд (pk={faculty})')
            return r[0]


    def get_student(self, student_id):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            select *
            from student
            where id = %s
            ''', student_id)

            r = cursor.fetchone()
            if r is None:
                raise Exception(f'Не найдено записей в бд (pk={student_id})')
            return {'id': r[0], 'name': r[1], 'faculty': r[2]}

    def get_courses_ids_by_names(self, names):
        if len(names) == 0:
            return {}
        res = {}
        with self.connection.cursor() as cursor:
            cursor.execute('''
            select * 
            from course 
            where name in %s
            ''', (names,))

            rs = cursor.fetchall()
            for r in rs:
                res[r[1]] = r[0]

        return res

    def save_mark(self, student_id, course_id, module, value):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            insert into mark(student_id, course_id, module, value) 
            values (%s, %s, %s, %s)
            ''', (student_id, course_id, module, value))

        return 1

    def get_student_marks(self, student_id):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            select m.value
            from course c
                left join (
                    select m.*
                    from mark m
                        left join mark m2 on m.student_id = m2.student_id
                                         and m.course_id = m2.course_id
                                         and m.module < m2.module
                    where m2 is null
                ) m on c.id = m.course_id
            where m is null or m.student_id = %s
            order by c.id
            ''', (student_id,))

            rs = cursor.fetchall()
            print(type(rs))
            print(rs)

