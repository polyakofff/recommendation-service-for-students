create table if not exists faculty (
    name text primary key
);

create table if not exists degree (
    name text primary key
);

create table if not exists student (
    id text primary key
);

create table if not exists subject (
    id text primary key,
    name text not null
);

create table if not exists mark (
    id serial primary key,
    student_id text not null references student (id),
    subject_id text not null references subject (id),
    module int not null,
    value int not null,
    unique (student_id, subject_id, module)
);

