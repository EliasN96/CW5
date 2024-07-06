from .base import DBManager
import psycopg2


class PostgresDBManager(DBManager):
    """
    Класс определяющий методы для работы с БД
    """
    def connect(self) -> None:
        """
        Метод, который подключает к БД, если она еще не подключена
        """
        if self.connection is None:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

    def disconnect(self) -> None:
        """
        Метод, который отключается от БД, если она подключена
        """
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_companies_and_vacancies_count(self) -> list[tuple[str, int]]:
        """
        Метод для получения компаний и кол-ва их вакансий
        """
        sql = """
            SELECT e.name, COUNT(*)
            FROM employers as e
            LEFT JOIN vacancies as v ON e.id = v.employer_id
            GROUP BY e.name
        """
        self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def get_avg_salary(self):
        """
        Метод для получения средней зарплаты по вакансиям
        """
        sql = """
            SELECT AVG(v.salary_from), AVG(v.salary_to) FROM vacancies AS v;
        """

        self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            min_salary, max_salary = cursor.fetchone()
            average_salary = (min_salary + max_salary) / 2
            return round(average_salary, 2)

    def get_vacancies_with_higher_salary(self):
        """
        Метод для получения вакансий с минимальной зарплатой выше средней по всем вакансиям
        """
        sql = """
            SELECT v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies AS v
            WHERE (v.salary_to + v.salary_from) / 2 > (SELECT AVG((salary_to + salary_from) / 2) FROM vacancies)
            AND v.salary_from > (SELECT AVG((salary_to + salary_from) / 2) FROM vacancies)
            GROUP BY v.name, v.salary_from, v.salary_to, v.url
            ORDER BY v.salary_from DESC;
        """
        self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def get_vacancies_with_keyword(self):
        """
        Метод для получения вакансий по ключевому слову
        """
        sql = """
            SELECT v.name, v.salary_from, v.salary_to, v.url FROM vacancies AS v
            WHERE v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL
            GROUP BY v.name, v.salary_from, v.salary_to, v.url
            ORDER BY v.salary_from DESC;
        """
        self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def get_all_vacancies(self):
        """
        Метод для получения всех вакансий
        """
        sql = """
            SELECT employers.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies AS v
            INNER JOIN employers ON v.employer_id=employers.id
            GROUP BY employers.name, v.name, v.salary_from, v.salary_to, v.url
            HAVING v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL
            ORDER BY v.salary_from DESC
        """
        self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
