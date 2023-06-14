create table if not exists student (
    id serial primary key,
    name text not null
);

create table if not exists course (
    id serial primary key,
    name text not null
);

create table if not exists mark (
    id serial primary key,
    student_id int references student (id),
    course_id int references course (id),
    module int not null,
    value int not null
);
