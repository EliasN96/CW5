from src.api_clients import HeadHunterAPIClient
from src.config import settings
from src.db.managers import PostgresDBManager
from tqdm import tqdm
api_client = HeadHunterAPIClient()


def load_employers():
    """
    Метод для загрузки работодателей через БД
    """
    employer_ids = settings.get_employer_ids()
    sql = """
        INSERT INTO employers (id, name, url, site_url, region)
        VALUES(%s, %s, %s, %s, %s)
    """

    db_manager = PostgresDBManager()
    db_manager.connect()

    try:
        with db_manager.connection.cursor() as cursor:
            for employer_id in tqdm(employer_ids, desc='Загрузка работодателей...'):
                emp = api_client.get_employer_info(employer_id)
                cursor.execute(sql, (emp.id, emp.name, emp.url, emp.site_url, emp.region))

            db_manager.commit()
    finally:
        db_manager.disconnect()


def load_vacancies():
    """
    Метод для загрузки вакансий через БД
    """
    employer_ids = settings.get_employer_ids()
    sql = """
            INSERT INTO vacancies (id, name, url, type, salary_from, salary_to, employer_id)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
        """

    db_manager = PostgresDBManager()
    db_manager.connect()

    try:
        with db_manager.connection.cursor() as cursor:
            for employer_id in tqdm(employer_ids, desc='Загрузка вакансий...'):
                vacancies = api_client.get_employer_vacancies(employer_id)
                data = (
                    (vac.id, vac.name, vac.url, vac.type.name, vac.salary_from, vac.salary_to, employer_id)
                    for vac in vacancies
                )
                cursor.executemany(sql, data)

            db_manager.commit()
    finally:
        db_manager.disconnect()
