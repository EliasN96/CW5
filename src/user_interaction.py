from src.db.managers import PostgresDBManager
from prettytable import PrettyTable


def run_interaction():
    """
    Метод для запуска интерактива для пользователя.
    Пользователь может выбрать действие, а программа возвращает запрошенные данные
    """
    user_actions = {
        '1': print_employers,
        '2': print_all_vacancies,
        '3': print_avg_salary,
        '4': print_vacancies_with_higher_salary,
        '5': print_vacancies_with_keyword
    }
    while True:
        print(
            'Выберите что сделать:',
            '1 - получить список всех компаний и количество вакансий у каждой компании;',
            '2 - получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки',
            '3 - получить среднюю зарплату по вакансиям;',
            '4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям;',
            '5 - получить список всех вакансий по ключевому слову',
            '0 - выйти',
            sep='\n'
        )
        user_input = input()

        if user_input == '0':
            break
        elif user_input in user_actions:
            handler = user_actions[user_input]
            handler()
        else:
            print('Вы ввели неверно, попробуйте еще:\n')


def print_employers():
    """
    Метод для печати работодателей
    """
    db_manager = PostgresDBManager()
    try:
        res = db_manager.get_companies_and_vacancies_count()
    finally:
        db_manager.disconnect()
    table = PrettyTable(field_names=['Название компании', 'Количество вакансий'])
    for data in res:
        table.add_row([data[0], data[1]])

    print(table)


def print_avg_salary():
    """
    Метод для печати средней зарплаты
    """
    db_manager = PostgresDBManager()
    try:
        salary = db_manager.get_avg_salary()
    finally:
        db_manager.disconnect()
    print(f'\nСредняя зарплата: {salary}\n')


def print_vacancies_with_higher_salary():
    """
    Метод для печати вакансий с минимальной зарплатой выше средней
    """
    db_manager = PostgresDBManager()
    try:
        higher_salary = db_manager.get_vacancies_with_higher_salary()
    finally:
        db_manager.disconnect()
    table = PrettyTable(field_names=['Название вакансии', 'Зарплата "от"', 'Зарплата "до"', 'Ссылка на вакансию'])
    for salary in higher_salary:
        table.add_row([salary[0], salary[1], salary[2], salary[3]])
    print(table)


def print_vacancies_with_keyword():
    """
    Метод для печати вакансий по ключевому слову
    """
    db_manager = PostgresDBManager()
    try:
        keyword = db_manager.get_vacancies_with_keyword()
    finally:
        db_manager.disconnect()
    table = PrettyTable(field_names=['Название вакансии', 'Зарплата "от"', 'Зарплата "до"', 'Ссылка на вакансию'])
    user_input = input("Введите ключевое слово для поиска вакансии:\n")
    for k in keyword:
        if user_input in k[0]:
            table.add_row([k[0], k[1], k[2], k[3]])

    print(table)


def print_all_vacancies():
    """
    Метод для печати всех вакансий
    """
    db_manager = PostgresDBManager()
    try:
        all_vacancies = db_manager.get_all_vacancies()
    finally:
        db_manager.disconnect()
    table = PrettyTable(
        field_names=['Работодатель', 'Вакансия', 'Зарплата "от"', 'Зарплата "до"', 'Ссылка на вакансию'])
    for v in all_vacancies:
        table.add_row([v[0], v[1], v[2], v[3], v[4]])

    print(table)
