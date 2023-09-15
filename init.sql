create table if not exists faculty (
    name text primary key
);

create table if not exists degree (
    name text primary key
);

create table if not exists student (
    id int primary key,
    faculty text not null references faculty (name),
    degree text not null references degree (name)
);

create table if not exists subject (
    id serial primary key,
    name text not null,
    faculty text not null references faculty (name),
    degree text not null references degree (name)
);

create table if not exists mark (
    id serial primary key,
    student_id int not null references student (id),
    subject_id int not null references subject (id),
    module int not null,
    value int not null,
    unique (student_id, subject_id, module)
);

