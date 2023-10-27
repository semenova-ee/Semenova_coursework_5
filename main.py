import psycopg2
import requests
from DBManager import DBManager
from config import config

empls_list = [
    1122462,
    3529,
    4934,
    999442,
    5088268,
    5382804,
    4307094,
    11463,
    1517303
]
# 'https://api.hh.ru/employers/{employer_id}'
# url = 'https://api.hh.ru/employers/1122462'
# headers = {'User-Agent': 'api-test-agent'}
# r = requests.get(url=url, headers=headers)
# responce = r.json()
# print(responce['id'])
# print(responce['name'])
# print(responce['open_vacancies'])
class APIManager():
    url = 'https://api.hh.ru/employers/'
    headers = {'User-Agent': 'api-test-agent'}
    def __init__(self, empls_list):
        self.empls_list = empls_list
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

    def get_employers(self, id: int):
        """Получает вакансии"""
        r = requests.get(self.url + str(id), headers=self.headers)
        return r.json()

    def save_employers_info(self):
        conn = self.setup_connection()
        with conn.cursor() as cur:
            for i in self.empls_list:
                responce = self.get_employers(i)
                cur.execute(
                    'INSERT INTO employees (employee_id, company_name, open_vacancies)'
                    'VALUES (%s, %s, %s)',
                    [int(responce["id"]), responce["name"], int(responce["open_vacancies"])]
                )


apimanager = APIManager(empls_list)
apimanager.save_employers_info()