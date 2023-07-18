from src.jobparser import *
from itertools import chain


class JobOperations:
    """Класс для сбора данных с сайтов с работой, использует для работы с API классы из jobparser"""

    JOB_SOURCE = {1: HHParser(), 2: SJParser()}  # словарь с объектами-парсерами (можно добавить, если будут ещё API)

    def __init__(self):
        self.cities_id = {}
        self.city_name = 'Москва'  # Город для поиска по умолчанию
        self.key_words = ''  # ключевое слово для поиска по умолчанию

    def get_city(self, user_city):
        """
        Загружает с HH и SJ списки доступных городов с id, пытается найти совпадение с городом,
        который указал пользователь. Если совпадений нет, возвращает None. Если есть одно совпадение, возвращает
        кортеж (True, название_города) и сохраняет в self.cities_id номер парсера из JOB_SOURCE и id города для него.
        Если есть несколько совпадений, возвращает кортеж (False, [список городов с похожими названиями])
        """
        if not user_city:
            user_city = self.city_name
        # получаем словарь всех доступных городов на каждом сайте
        # {номер парсера в job_sources: {город: id, город: id,...}}
        all_cities_job_sources = {job_source: parser.get_cities() for job_source, parser in self.JOB_SOURCE.items()}
        found_cities = {}
        # получаем словарь с соответствиями введённому пользователем названию
        # {номер ресурса в job_sources: [список подходящих городов]}
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
            self.city_name = [i[0] for i in found_cities.values() if i][0]
            return True, self.city_name

        # если найдено более одного города на каждом ресурсе возвращаем список всех найденных городов
        return False, list(set(chain(*found_cities.values())))

    def load_vacancies(self, key_words):
        """Возвращает массив объектов Vacancy с найденными на HH и SJ вакансиями"""
        self.key_words = key_words
        vacancies = []
        for job_source, parser in self.JOB_SOURCE.items():
            if self.cities_id[job_source]:
                vacancies.extend(parser.get_vacancies(self.cities_id[job_source], self.key_words))
        return vacancies
