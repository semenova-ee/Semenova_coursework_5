# Курсовая работа 5. БД

## Реализация задания
Написана программа, которая получает данные о работодателях и их вакансиях с сайта hh.ru. 
И реализован код, который заполняет созданные в БД PostgreSQL таблицы полученными данными.
## Структура проекта
Файл **DBManager** содержит класс **DBManager**  для работы с БД PostgreSQL. Класс имеет 1 staticmethod и 5 методов, позволяющих:
1. Получить список всех компаний и  количество вакансий у каждой компании.
2. Получить писок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
3. Получить среднюю зарплату по вакансиям.
4. Получить  список всех вакансий, у которых зарплата выше средней по всем вакансиям.
5. Получить список всех вакансий, в названии/необходимых навыках которых содержатся переданные в метод слова
Файл **main** содержит класс **APIManager**, в котором
   реализованы методы для запроса информации о вакансиях и работодателях и получения информации о вакансии, работодателе, зарплате.
## Работа с проектом
1. Необходимо в pgAdmin создать БД и таблицы "emploeeys" и "vacancies" (с связью один ко многим от "emploeeys" к "vacancies").
2.  Создать виртуальное окружение и активировать его.
3. Установить необходимые библиотеки.
4. Для заполнения таблиц в БД необходимо ввести переменные в **main** (Достаточно раскомментировать), например,
   
`apimanager = APIManager(empls_list)`

`apimanager.save_employers_info()`

`apimanager.save_vacancy_info()`

Предполагаемый результат:

![image](https://github.com/semenova-ee/Semenova_coursework_5/assets/141341489/7d28dbef-8cb7-4d05-ae49-d5dbafac6697)

и

![image](https://github.com/semenova-ee/Semenova_coursework_5/assets/141341489/4266cd72-0132-4b34-8223-d9a8784b6359)

5. Для получения списка вакансий, у которых з/п выше средней, ввести в **DBManager** (достаточно раскомментировать), например,

`vacancies_list = DBManager()`

`for i in vacancies_list.get_vacancies_with_higher_salary():`

`print(i)`
    
Предполагаемый результат:

![image](https://github.com/semenova-ee/Semenova_coursework_5/assets/141341489/bc143b44-8c91-4400-a32c-639acb9cef54)


6. Для получения списка вакансий, в названии которых содержится ключевое слово, ввести в **DBManager** (достаточно раскомментировать):

`vacancies_with_keyword_list = DBManager()`

`for i in vacancies_with_keyword_list.get_vacancies_with_keyword('Developer'):`

`print(i)`
    
Предполагаемый результат:

![image](https://github.com/semenova-ee/Semenova_coursework_5/assets/141341489/6b524460-505f-482d-929b-7c558636fd56)


7. Для получения списка вакансий, в необходимых навыках которых содержится ключевое слово, ввести в **DBManager** (достаточно раскомментировать):
   
`vacancies_with_skills_keyword_list = DBManager()`

`for i in vacancies_with_skills_keyword_list.get_vacancies_with_skills_keyword('Python'):`

`print(i)`
    
Предполагаемый результат:

![image](https://github.com/semenova-ee/Semenova_coursework_5/assets/141341489/72967b42-297e-4004-bfbb-40bf9860c245)

