# Курсовая работа 5. БД

## Реализация задания
Написана программа, которая получает данные о работодателях и их вакансиях с сайта hh.ru. 
И реализован код, который заполняет созданные в БД PostgreSQL таблицы полученными данными.
## Структура проекта
1. Файл **DBManager** содержит класс **DBManager**  для работы с БД PostgreSQL. Класс имеет 1 staticmethod и 5 методов, позволяющих:
2. Получить список всех компаний и  количество вакансий у каждой компании.
3. Получить писок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
4. Получить среднюю зарплату по вакансиям.
5. Получить  список всех вакансий, у которых зарплата выше средней по всем вакансиям.
6. Получить список всех вакансий, в названии которых содержатся переданные в метод слова
7. Файл **main** содержит класс **APIManager**, в котором
   реализованы методы для запроса информации о вакансиях и работодателях и получения информации о вакансии, работодателе, зарплате.
## Работа с проектом
Необходимо в pgAdmin создать БД и таблицы "emploeeys" и "vacancies" (с связью один ко многим от "emploeeys" к "vacancies").
Создать виртуальное окружение и активировать его.
Установить необходимые библиотеки.
Для заполнения таблиц в БД необходимо ввести переменные в **main**, например,
apimanager = APIManager(empls_list)
apimanager.save_employers_info()
apimanager.save_vacancy_info()

Для получения списка вакансий, у которых з/п выше средней ввести переменные в **DBManager**, например,
vacancies_list = DBManager()
for i in vacancies_list.get_vacancies_with_higher_salary():
    print(i)
Предполагаемые результат:
![image](https://github.com/semenova-ee/Semenova_coursework_5/assets/141341489/bc143b44-8c91-4400-a32c-639acb9cef54)

