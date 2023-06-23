CREATE TABLE public."degree" (
	degree_id int4 NOT NULL,
	degree_name varchar NOT NULL,
	degree_tag varchar NOT NULL,
	CONSTRAINT degree_pkey PRIMARY KEY (degree_id)
);



CREATE TABLE public.faculty (
	faculty_id int4 NOT NULL,
	faculty_name varchar NOT NULL,
	faculty_tag varchar NOT NULL,
	CONSTRAINT faculty_pkey PRIMARY KEY (faculty_id)
);



CREATE TABLE public."program" (
	program_id int4 NOT NULL,
	program_name varchar NOT NULL,
	CONSTRAINT program_pkey PRIMARY KEY (program_id)
);


CREATE TABLE public.subject (
	subject_id varchar NOT NULL,
	subject_name varchar NOT NULL,
	CONSTRAINT subject_pkey PRIMARY KEY (subject_id)
);


CREATE TABLE public.student (
	student_id int4 NOT NULL,
	faculty_id int4 NOT NULL,
	degree_id int4 NOT NULL,
	program_id int4 NULL,
	CONSTRAINT student_pkey PRIMARY KEY (student_id),
	CONSTRAINT student_degree_id_fkey FOREIGN KEY (degree_id) REFERENCES public."degree"(degree_id),
	CONSTRAINT student_faculty_id_fkey FOREIGN KEY (faculty_id) REFERENCES public.faculty(faculty_id),
	CONSTRAINT student_program_id_fkey FOREIGN KEY (program_id) REFERENCES public."program"(program_id)
);