from functools import total_ordering
import json
import re


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
        """Возвращает строку с описанием вакансии"""
        # Выбираем, что написать в сумме зп в зависимости от наличия данных
        if self.salary_from == 0 and self.salary_to == 0:
            vacancy_salary = 'не указана'
        elif self.salary_to == 0 and self.salary_from != 0:
            vacancy_salary = f'{self.salary_from} рублей в месяц'
        elif self.salary_to != 0 and self.salary_from == 0:
            vacancy_salary = f'до {self.salary_to} рублей в месяц'
        else:
            vacancy_salary = f'от {self.salary_from} до {self.salary_to} рублей в месяц'

        # В описании вакансии встречаются очень длинные строчки, вылавливаем их и режем по 15 слов
        responsibility = self.responsibility + ' ' + self.requirement if self.requirement else self.responsibility
        tmp_text_list = responsibility.split('\n')
        for i in range(len(tmp_text_list)):
            if tmp_text_list[i].count(' ') > 15:
                tmp_text_list[i] = re.sub(r'((\S*\s){15})', r'\1\n', tmp_text_list[i])
        responsibility = '\n'.join(tmp_text_list)

        vacancy_str = f"Вакансия: {self.name}\n" \
                      f"Компания: {self.company}\n" \
                      f"Зарплата: {vacancy_salary}\n" \
                      f"Задачи и требования к кандидату: {responsibility}\n" \
                      f"Ссылка: {self.url}"
        return vacancy_str

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return max(self.salary_from, self.salary_to) == max(other.salary_from, other.salary_to)

        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, type(self)):
            return max(self.salary_from, self.salary_to) > max(other.salary_from, other.salary_to)
        return NotImplemented

    def jsonify(self):
        """Возвращает json строку представление объекта Vacancy, нужна для сериализации и сохранения"""
        return json.dumps(self.__dict__, indent=4)

    def unjsonify(self, jsobj):
        """Возвращает объект Vacancy инициированный из json строки"""
        new = type(self)()
        new.__dict__.update(json.loads(jsobj))
        return new
