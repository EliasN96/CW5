from dataclasses import dataclass
from enum import Enum


@dataclass
class ShortEmployerInfo:
    id: int
    name: str
    url: str
    open_vacancies: int


@dataclass
class FullEmployerInfo:
    id: int
    name: str
    url: str
    site_url: str
    region: str
    open_vacancies: int


class VacancyType(Enum):
    open = "Открытая"
    closed = "Закрытая"
    anonymous = "Анонимная"
    direct = "Рекламная"


@dataclass
class VacancyInfo:
    id: int
    name: str
    url: str
    salary_from: int | None
    salary_to: int | None
    employer_id: int
    type: VacancyType | None
