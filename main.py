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
    url_employers = 'https://api.hh.ru/employers/'
    url_vacancy = 'https://api.hh.ru/vacancies/'
    url_list_of_vacancies = 'https://api.hh.ru/vacancies?employer_id='
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

    def send_request(self, id: int, for_vacancies: bool = False, for_current_vacancy: bool = False):
        """Получает вакансии"""
        if for_vacancies:
            r = requests.get(self.url_list_of_vacancies + str(id), headers=self.headers)
            return r.json()
        elif for_current_vacancy:
            r = requests.get(self.url_vacancy + str(id), headers=self.headers)
            return r.json()
        r = requests.get(self.url_employers + str(id), headers=self.headers)
        return r.json()

    def save_employers_info(self):
        conn = self.setup_connection()
        with conn.cursor() as cur:
            for i in self.empls_list:
                responce = self.send_request(i)
                cur.execute(
                    'INSERT INTO employees (employee_id, company_name, open_vacancies)'
                    'VALUES (%s, %s, %s)',
                    [int(responce["id"]), responce["name"], int(responce["open_vacancies"])]
                )

    def save_vacancy_info(self):
        conn = self.setup_connection()
        with conn.cursor() as cur:
            for i in self.empls_list:
                responce = self.send_request(i, True)
                items = responce['items']
                for item in items:
                    res = self.send_request(item['id'], for_current_vacancy = True)
                    salary = self.inspect_salary(res)
                    if salary:
                        cur.execute(
                        'INSERT INTO vacancies (employee_id, company_name, open_vacancies)'
                        'VALUES (%s, %s, %s)',
                        [int(responce["id"]), responce["name"], int(responce["open_vacancies"])]
                        )

    @staticmethod
    def inspect_salary(vacancy: dict) -> int or None:
        try:
            if vacancy['salary']['currency'] != "RUR":
                return None
            from_salary = vacancy["salary"]["from"]
            to_salary = vacancy["salary"]["to"]
            if vacancy["salary"] is None:
                return None
            elif from_salary and to_salary:
                return int(from_salary)
            elif from_salary:
                return int(from_salary)
            else:
                return None
        except Exception:
            return None


apimanager = APIManager(empls_list)
apimanager.save_employers_info()