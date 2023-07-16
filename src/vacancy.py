from abc import ABC, abstractmethod

class Vacancy(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_param_string(self):
        pass


class SJVacancy(Vacancy):
    def __init__(self):
        pass
