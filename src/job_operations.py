from JobParser import *
import pprint
from itertools import chain


class JobOperations:
    """Класс для сбора данных с сайтов с работой"""

    JOB_SOURCE = {1: HHParser(), 2: SJParser()}  # словарь с объектами-парсерами (можно добавить, если будут ещё API)

    def __init__(self):
        self.cities_id = {}
        self.job_city = 'Москва'
        self.key_words = []


    def get_city(self):
        """
        Определяет город, по которому будем парсить вакансии и возвращает словарь с id города в виде
        {номер парсера в job_sources: id города, специфичный для конкретного сайта}
        """
        while True:
            print('По умолчанию поиск производится в Москве, для перехода к поиску вакансий в Москве просто нажмите Enter')
            user_city = input('Введите название(или его часть) города: ')
            if not user_city:
                user_city = self.job_city
            #получаем словарь всех доступных городов на каждом сайте {номер парсера в job_sources: {город: id, город: id,...}}
            all_cities_job_sources = {job_source: parser.get_cities() for job_source, parser in self.JOB_SOURCE.items()}
            found_cities = {}
            #получаем словарь с соответствиями введённому пользователем названию {номер ресурса в job_sources: [список подходящих городов]}
            for job_source in all_cities_job_sources:
                found_cities[job_source] = list(c for c in all_cities_job_sources[job_source]
                                                if c.lower().find(user_city.lower()) != -1)

            #если ничего не найдено
            if all(True if not len(i) else False for i in found_cities.values()):
                print('По Вашему запросу ничего не найдено, попробуйте ещё раз.')
                continue

            #если на каждом ресурсе найдено не более одного города с названием, указанным пользователем
            #возвращаем словарь {номер парсера в job_sources: city_id}
            if all(True if len(i) <= 1 else False for i in found_cities.values()):
                self.cities_id = {job_source: (all_cities_job_sources[job_source][city_list[0]]
                                     if len(city_list) == 1 else None) for job_source, city_list in found_cities.items()}
                self.job_city = user_city
                return True

            # если найдено более одного города на каждом ресурсе выбираем из подходящих городов нужный
            found_cities_general_dict = dict(enumerate(set(chain(*found_cities.values()))))
            print('По Вашему запросу найдены следующие города (введите номер нужного города)\n',
                  '(выход - чтобы выйти, повторить - чтобы повторить ввод названия города):')
            print('\n'.join(f'{n} - {c}' for n, c in found_cities_general_dict.items()))
            while True:
                city_number = input()
                if city_number.lower() == 'выход':
                    return False
                if city_number.lower() == 'повторить':
                    break
                if not city_number.isdigit() or int(city_number) < 0 or int(city_number) > len(found_cities_general_dict):
                    print('Введите номер одного из найденных городов\n',
                          '(выход - чтобы выйти, повторить - чтобы повторить ввод названия города):')
                else:
                    final_city = found_cities_general_dict[int(city_number)]
                    # возвращаем словарь {номер парсера в job_sources: city_id}
                    self.cities_id = {job_source: (all_cities_job_sources[job_source].get(final_city, None))
                                      for job_source, city_list in found_cities.items()}
                    self.job_city = final_city
                    return True

    def load_data(self):
        pass

    def get_key_words(self):
        """Берёт у пользователя ключевые слова для поиска"""
        print('Введите ключевые слова для поиска (например программист python):')
        self.key_words = input()


if __name__ == '__main__':
    a = JobOperations()
    a.get_city()
    print(a.cities_id)