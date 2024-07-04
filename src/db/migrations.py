from pathlib import Path

import psycopg2
from src.config import settings
from src.db.managers import PostgresDBManager


def create_database():
    db_manager = PostgresDBManager(db_name='postgres')
    db_manager.connect()
    db_manager.connection.autocommit = True

    try:
        with db_manager.connection.cursor() as cursor:
            cursor.execute(f'DROP DATABASE IF EXISTS {settings.DB_NAME}')
            cursor.execute(f'CREATE DATABASE {settings.DB_NAME}')
    finally:
        db_manager.disconnect()


def apply_migrations():
    db_manager = PostgresDBManager()
    db_manager.connect()

    try:
        with db_manager.connection.cursor() as cursor:
            for migration in sorted(settings.MIGRATIONS_DIR.glob('*sql')):
                cursor.execute(_read_migration(migration))
            db_manager.commit()
    finally:
        db_manager.disconnect()


def _read_migration(file_path: Path) -> str:
    with file_path.open(encoding='UTF-8') as f:
        return f.read()
