import psycopg2 as psycopg2
from config import config


class DBManager():

    @staticmethod
    def setup_connection():
        params = config()
        conn = None
        try:
            with psycopg2.connect(**params) as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    return cur
        except psycopg2.Error as e:
            print(f"PostgreSQL error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn is not None:
                conn.close()

    def get_companies_and_vacancies_count(self):
        cur = self.setup_connection()
        cur.execute('SELECT company_name, open_vacancies FROM employees')
        return cur.fetchall()

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        cur = self.setup_connection()
        cur.execute('SELECT AVG(salary) FROM vacancies')
        return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass



