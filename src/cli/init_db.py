from src.db.loader import load_employers, load_vacancies
from src.db.migrations import create_database, apply_migrations


def run():
    """
    Метод создающий БД, запускающий инициализацию загрузки работодателей и вакансий
    """
    print('Создание схем...')
    create_database()
    apply_migrations()
    load_employers()
    load_vacancies()


if __name__ == '__main__':
    run()
