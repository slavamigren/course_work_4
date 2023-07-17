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
        pass

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
        """Формирует список с вакансиями в сущностях Vacancy"""
        vacancies = []  # сюда сохраняем список вакансий
        for page in range(20):  # Берём 20 страниц поиска по 100 вакансий, тк HH выдаёт по API только 2000 вакансий
            params = {
                'text': key_words,  # Ключевые слова для поиска
                'area': city_id,  # Индекс города
                'page': page,  # Индекс страницы поиска на HH
                'per_page': 100  # Максимальное кол-во вакансий на 1 странице
            }

            try:
                response = requests.get('https://api.hh.ru/vacancies', params)
            except requests.exceptions.HTTPError as err:
                print(f'Соединение с HH недоступно, ошибка: {err}')

            data = response.content.decode('utf-8')
            jsobj = json.loads(data)
            #считываем нужные поля в полученной информации, сразу очищаем от html тегов
            for vacancy in jsobj['items']:
                vacancies.append(Vacancy(vacancy['name'],
                                              vacancy['salary']['from'] if vacancy['salary'] is not None else None,
                                              vacancy['salary']['to'] if vacancy['salary'] is not None else None,
                                              re.sub(r'<.+?>', '', vacancy['snippet']['responsibility']) if
                                              vacancy['snippet']['responsibility'] is not None else '-',
                                              re.sub(r'<.+?>', '', vacancy['snippet']['requirement']) if
                                              vacancy['snippet']['requirement'] is not None else '-',
                                              vacancy['employer']['name'],
                                              vacancy['alternate_url']))
            time.sleep(0.2)  # Задержка, чтобы API не выбрасывал ошибку и не блокировать наш IP
        return vacancies



class SJParser(JobParser):
    """Класс для парсинга SJ"""
    API_KEY = 'v3.r.137683485.9c1f43e97d89af87146f830f597088ad551686c3.4082fa3c04252a5cfd13e7794230aa13081f4409'
    HEADER = {'X-Api-App-Id': API_KEY}

    def __init__(self):
        pass

    def get_cities(self):
        """Возвращает словарь доступных на SJ городов {'название города': 'id города'}"""
        params = {'all': 'True'}
        try:
            response = requests.get('https://api.superjob.ru/2.0/towns/', params, headers=self.HEADER)
        except requests.exceptions.HTTPError as err:
            print(f'Соединение с SJ недоступно, ошибка: {err}')
        return {i['title']: i['id'] for i in response.json()['objects']}

    def get_vacancies(self, city_id, key_words):
        """Формирует список с вакансиями в сущностях Vacancy"""
        vacancies = []  # сюда сохраняем список вакансий
        for page in range(25):  # Берём 25 страниц поиска по 20 вакансий, тк SJ выдаёт по API только 500 вакансий
            params = {'town': city_id,
                      'page': page,
                      'keyword': key_words.strip().split()
                      }
            try:
                response = requests.get('https://api.superjob.ru/2.0/vacancies/', params, headers=self.HEADER)
            except requests.exceptions.HTTPError as err:
                print(f'Соединение с SJ недоступно, ошибка: {err}')

            data = response.content.decode()
            jsobj = json.loads(data)

            for vacancy in jsobj['objects']:
                vacancies.append(Vacancy(vacancy['profession'],
                                              vacancy['payment_from'] if vacancy['payment_from'] != 0 else None,
                                              vacancy['payment_to'] if vacancy['payment_to'] != 0 else None,
                                              vacancy['candidat'],
                                              None,
                                              vacancy['firm_name'],
                                              vacancy['link']))
            time.sleep(0.2)
        return vacancies


if __name__ == "__main__":
    a = HHParser()
    #a.get_cities()
    a.get_vacancies(4, 'коммерческий директор')