from functools import total_ordering
import json

@total_ordering
class Vacancy:
    def __init__(self, name=None,
                 salary_from=None,
                 salary_to=None,
                 responsibility=None,
                 requirement=None,
                 company=None,
                 url=None):

        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.responsibility = responsibility
        self.requirement = requirement
        self.company = company
        self.url = url

    def __str__(self):
        if self.salary_from is None and self.salary_to is None:
            vacancy_salary = 'не указана'
        elif self.salary_to is None:
            vacancy_salary = f'{self.salary_from} рублей в месяц'
        else:
            vacancy_salary = f'от {self.salary_from} до {self.salary_to} рублей в месяц'

        responsibility = self.responsibility + ' ' + self.requirement if self.requirement else self.responsibility

        vacancy_str = f"""Вакансия: {self.name}
Компания: {self.company}
Зарплата: {vacancy_salary}
Задачи и требования к кандидату: {responsibility}
Ссылка: {self.url}
"""
        return vacancy_str

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.salary_from and other.salary_from:
                return self.salary_from == other.salary_from
            else:
                return False
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, type(self)):
            if self.salary_from and other.salary_from:
                return self.salary_from < other.salary_from
            else:
                return False
        return NotImplemented

    def jsonify(self):
        return json.dumps(self.__dict__, indent=4)

    def unjsonify(self, jsobj):
        new = type(self)()
        new.__dict__.update(json.loads(jsobj))
        return new

#if __name__ == '__main__':
#    with open('qqqq.json', 'r') as file:
#        s = json.load(file)
#    ggg = []
#    for i in s:
#        ggg.append(Vacancy().unjsonify(i))
#    for i in ggg:
#        print(i)