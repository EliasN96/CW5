from dataclasses import dataclass
from enum import Enum


@dataclass
class ShortEmployerInfo:
    """
    Дата класс с обозначением параметров для краткой информации о работодателе
    """
    id: int
    name: str
    url: str
    open_vacancies: int


@dataclass
class FullEmployerInfo:
    """
    Дата класс с обозначением параметров для полной информации о работодателе
    """
    id: int
    name: str
    url: str
    site_url: str
    region: str
    open_vacancies: int


class VacancyType(Enum):
    """
    Класс определяющий типы вакансий
    """
    open = "Открытая"
    closed = "Закрытая"
    anonymous = "Анонимная"
    direct = "Рекламная"


@dataclass
class VacancyInfo:
    """
    Дата класс с обозначением параметров для информации о вакансии
    """
    id: int
    name: str
    url: str
    salary_from: int | None
    salary_to: int | None
    employer_id: int
    type: VacancyType | None
