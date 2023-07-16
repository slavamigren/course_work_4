from abc import ABC, abstractmethod


class CytyList(ABC):
    """Класс для хранения списка и id городов, доступных на ресурсе"""
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_city_id(self):
        pass