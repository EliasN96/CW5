from .base import DBManager
import psycopg2


class PostgresDBManager(DBManager):
    def connect(self) -> None:
        if self.connection is None:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

    def disconnect(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_companies_and_vacancies_count(self) -> list[tuple[str, int]]:
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
