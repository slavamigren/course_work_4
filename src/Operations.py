from src.JobParser import *
import pprint
from itertools import chain
from DataOperations import VacancyDataOperations


class JobOperations:
    """Класс для сбора данных с сайтов с работой"""

    JOB_SOURCE = {1: HHParser(), 2: SJParser()}  # словарь с объектами-парсерами (можно добавить, если будут ещё API)

    def __init__(self):
        self.cities_id = {}
        self.job_city = 'Москва'
        self.key_words = ''
        #self.vacancies = []
        self.all_data_object = VacancyDataOperations()


    def get_city(self, user_city):
        if not user_city:
            user_city = self.job_city
        # получаем словарь всех доступных городов на каждом сайте {номер парсера в job_sources: {город: id, город: id,...}}
        all_cities_job_sources = {job_source: parser.get_cities() for job_source, parser in self.JOB_SOURCE.items()}
        found_cities = {}
        # получаем словарь с соответствиями введённому пользователем названию {номер ресурса в job_sources: [список подходящих городов]}
        for job_source in all_cities_job_sources:
            found_cities[job_source] = list(c for c in all_cities_job_sources[job_source]
                                            if c.lower().find(user_city.lower()) != -1)
        # если ничего не найдено
        if all(True if not len(i) else False for i in found_cities.values()):
            return None

        # если на каждом ресурсе найдено не более одного города с названием, указанным пользователем
        # возвращаем словарь {номер парсера в job_sources: city_id}
        if all(True if len(i) <= 1 else False for i in found_cities.values()):
            self.cities_id = {job_source: (all_cities_job_sources[job_source][city_list[0]]
                                           if len(city_list) == 1 else None) for job_source, city_list in
                              found_cities.items()}
            self.job_city = [i[0] for i in found_cities.values() if i][0]
            return True, self.job_city

        # если найдено более одного города на каждом ресурсе возвращаем список всех найденных городов
        return False, list(set(chain(*found_cities.values())))

    def get_key_words(self, key_words):
        """Получает ключевые слова для поиска"""
        self.key_words = key_words

    def load_vacancies(self):  #  передаёт найденные на HH и SJ вакансии в объект DataOperations
        vacancies = []
        for job_source, parser in self.JOB_SOURCE.items():
            if self.cities_id[job_source]:
                vacancies.extend(parser.get_vacancies(self.cities_id[job_source], self.key_words))
        self.all_data_object.add_data(self.job_city, self.key_words, vacancies)






