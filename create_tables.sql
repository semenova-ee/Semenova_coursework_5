CREATE TABLE employees (
    employee_id integer PRIMARY KEY,
	company_name varchar (50),
	open_vacancies integer,
);
CREATE TABLE vacancies (
    vacancy_id integer PRIMARY KEY,
    vacancies_name varchar (100),
    salary integer,
    vacancy_link varchar,
    key_skills varchar,
    employee_id integer REFERENCES employees(employee_id)
);