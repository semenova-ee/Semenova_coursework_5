import psycopg2
import requests
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
    1517303,
    4046921
]


class APIManager:
    """Класс для работы с API"""
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
        """Посылает запрос для получения информации о вакансиях, работодателе"""
        if for_vacancies:
            r = requests.get(self.url_list_of_vacancies + str(id), headers=self.headers)
            return r.json()
        elif for_current_vacancy:
            r = requests.get(self.url_vacancy + str(id), headers=self.headers)
            return r.json()
        r = requests.get(self.url_employers + str(id), headers=self.headers)
        return r.json()

    def save_employers_info(self):
        """Получает информацию о работодателе"""
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
        """Получает информацию о вакансии"""
        conn = self.setup_connection()
        with conn.cursor() as cur:
            for i in self.empls_list:
                responce = self.send_request(i, True)
                items = responce['items']
                for item in items:
                    res = self.send_request(item['id'], for_current_vacancy=True)
                    salary = self.inspect_salary(res)
                    if salary:
                        cur.execute(
                            'INSERT INTO vacancies (vacancy_id, vacancies_name, salary, vacancy_link, key_skills, employee_id)'
                            'VALUES (%s, %s, %s, %s, %s, %s)',
                            [int(res["id"]), res["name"], salary, res["alternate_url"], [key_skill["name"] for key_skill in res["key_skills"]], res["employer"]["id"]]
                        )
                        print(f'вакансия {res["name"]} сохранена')

    @staticmethod
    def inspect_salary(vacancy: dict) -> int or None:
        """Получает информацию о заработной плате"""
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

# apimanager = APIManager(empls_list)
# apimanager.save_employers_info()
# apimanager.save_vacancy_info()
