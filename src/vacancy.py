from abc import ABC, abstractmethod

class Vacancy:
    def __init__(self, name, salary_from, salary_to, responsibility, requirement, company):
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.responsibility = responsibility
        self.requirement = requirement
        self.company = company

    def get_param_string(self):
        pass
