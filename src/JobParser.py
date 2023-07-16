from abc import ABC, abstractmethod
from vacancy import Vacancy
import requests
import pprint
from requests.exceptions import HTTPError
import json
import time
import os
import re


class JobParser(ABC):
    """Абстрактный класс для API работных сайтов"""
    @abstractmethod
    def __init__(self):
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
        self.vacancies = []
    def get_cities(self):
        """Возвращает словарь доступных на HH городов {'название города': 'id города'}"""
        try:
            response = requests.get('https://api.hh.ru/areas')
        except requests.exceptions.HTTPError as err:
            print(f'Соединение с HH недоступно, ошибка: {err}')

        cities_dict = {}
        for i in response.json():
            for j in i['areas']:
                cities_dict[j['name']] = j['id']
                for n in j['areas']:
                    cities_dict[n['name']] = n['id']
        return cities_dict


    def get_vacancies(self, city_id, key_words):
    """Формирует список с сущностями Vacancy"""

        for page in range(20):  #Берём 20 страниц поиска, тк HH выдаёт по API только 20 страниц
            params = {
                'text': key_words,  # Ключевые слова для поиска
                'area': city_id,  # Индекс города
                'page': page,  # Индекс страницы поиска на HH
                'per_page': 100  # Максимальное кол-во вакансий на 1 странице
            }
            response = requests.get('https://api.hh.ru/vacancies', params)
            data = response.content.decode('utf-8')
            jsobj = json.loads(data)
            for vacancy in jsobj['items']:
                self.vacancies.append(Vacancy(vacancy['name'],
                                              vacancy['salary']['from'] if vacancy['salary'] != None else None,
                                              vacancy['salary']['to'] if vacancy['salary'] != None else None,
                                              re.sub(r'<.+?>' , '', vacancy['snippet']['responsibility']) if vacancy['snippet']['responsibility'] != None else '-',
                                              re.sub(r'<.+?>' , '', vacancy['snippet']['requirement']) if vacancy['snippet']['requirement'] != None else '-',
                                              vacancy['employer']['name']))
            time.sleep(0.25)  #  задержка, чтобы API не выбрасывал ошибку и не блокировать наш IP





class SJParser(JobParser):
    """Класс для парсинга SJ"""
    API_KEY = 'v3.r.137683485.9c1f43e97d89af87146f830f597088ad551686c3.4082fa3c04252a5cfd13e7794230aa13081f4409'
    HEADER = {'X-Api-App-Id': API_KEY}

    def __init__(self):
        pass
    def get_cities(self):
        """Возвращает словарь доступных на SJ городов {'название города': 'id города'}"""
        key_words = {'all': 'True'}
        try:
            response = requests.get('https://api.superjob.ru/2.0/towns/', key_words, headers=self.HEADER)
        except requests.exceptions.HTTPError as err:
            print(f'Соединение с SJ недоступно, ошибка: {err}')

        return {i['title']: i['id_region'] for i in response.json()['objects']}


    def get_vacancies(self, city_id, key_words):
        pass


if __name__ == "__main__":
    a = HHParser()
    a.get_vacancies(1, 'программист python')