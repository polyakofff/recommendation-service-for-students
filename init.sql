create table if not exists faculty (
    name text primary key
);

create table if not exists student (
    id serial primary key,
    name text,
    faculty text not null references faculty (name)
);

create table if not exists course (
    id serial primary key,
    name text not null
);

create table if not exists mark (
    id serial primary key,
    student_id int not null references student (id),
    course_id int not null references course (id),
    module int not null,
    value int not null
);

create table if not exists faculty_model (
    faculty text primary key references faculty (name),
    model bytea not null
);
