from abc import ABC, abstractmethod


class JobParser(ABC):
    """Абстрактный класс для API работных сайтов"""
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def test_connection(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_cities(self):
        pass


class HHParser(JobParser):
    """Класс для парсинга HH"""

    def __init__(self):
        pass