import psycopg2 as psycopg2
from config import config


class DBManager:

    def __init__(self):
        self.conn = self.setup_connection()
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
        try:
            with self.conn.cursor() as cur:
                cur.execute('SELECT company_name, open_vacancies FROM employees;')
                return cur.fetchall()
        finally:
            self.conn.close()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
           названия вакансии и зарплаты и ссылки на вакансию."""
        conn = self.setup_connection()
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT E.company_name, V.vacancies_name, V.salary, V.vacancy_link FROM vacancies V \
                        JOIN employees E on V.employee_id = E.employee_id;')
                return cur.fetchall()
        finally:
            conn.close()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        try:
            with self.conn.cursor() as cur:
                cur.execute('SELECT AVG(salary) FROM vacancies;')
                return cur.fetchall()
        finally:
            self.conn.close()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        try:
            with self.conn.cursor() as cur:
                cur.execute('SELECT * FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies);')
                return cur.fetchall()
        finally:
            self.conn.close()

    def get_vacancies_with_skills_keyword(self, keyword: str):
        """Получает список всех вакансий по переданному ключевому слову в списке skills."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT * FROM vacancies WHERE '{keyword}' = ANY(key_skills);")
                return cur.fetchall()
        finally:
            self.conn.close()

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий по переданному ключевому слову в названии вакансии."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT * FROM vacancies WHERE vacancies_name LIKE '%{keyword}%';")
                return cur.fetchall()
        finally:
            self.conn.close()

# vacancies_list = DBManager()
# for i in vacancies_list.get_vacancies_with_higher_salary():
#     print(i)
# vacancies_with_keyword_list = DBManager()
# for i in vacancies_with_keyword_list.get_vacancies_with_keyword('Developer'):
#     print(i)
# vacancies_with_skills_keyword_list = DBManager()
# for i in vacancies_with_skills_keyword_list.get_vacancies_with_skills_keyword('Python'):
#     print(i)
