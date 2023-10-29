import psycopg2 as psycopg2
from config import config


class DBManager:
    @staticmethod
    def setup_connection():
        params = config()
        try:
            with psycopg2.connect(**params) as conn:
                conn.autocommit = True
                return conn
        except psycopg2.Error as e:
            print(f"PostgreSQL error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        conn = self.setup_connection()
        with conn.cursor() as cur:
            cur.execute('SELECT company_name, open_vacancies FROM employees;')
            return cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
           названия вакансии и зарплаты и ссылки на вакансию."""
        conn = self.setup_connection()
        with conn.cursor() as cur:
            cur.execute('SELECT E.company_name, V.vacancies_name, V.salary, V.vacancy_link FROM vacancies V \
                    JOIN employees E on V.employee_id = E.employee_id;')
            return cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        conn = self.setup_connection()
        with conn.cursor() as cur:
            cur.execute('SELECT AVG(salary) FROM vacancies;')
            return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = self.setup_connection()
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies);')
            return cur.fetchall()

    def get_vacancies_with_skills_keyword(self, keyword: str):
        """Получает список всех вакансий по переданному ключевому слову в списке skills."""
        conn = self.setup_connection()
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM vacancies WHERE '{keyword}' = ANY(key_skills);")
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий по переданному ключевому слову в названии вакансии."""
        conn = self.setup_connection()
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM vacancies WHERE vacancies_name LIKE '%{keyword}%';")
            return cur.fetchall()
