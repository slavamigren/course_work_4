import json
from abc import ABC, abstractmethod
from vacancy import Vacancy


class DataOperations(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_data(self, data, key_words, city):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def del_data(self, data_set_number):
        pass

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def unload_data(self):
        pass


class VacancyDataOperations(DataOperations):
    """Класс для сохранения, чтения, изменения и предоставления для анализа вакансий"""

    def __init__(self):
        with open('config.json', 'r') as file:  # подгружаем название файла с данными
            data = json.load(file)
            self.data_file = data['data_file']
        self.data = []
        self.load_data()

    def load_data(self):
        """Загружает сохранённые вакансии"""
        with open(self.data_file, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except:  # если файл пуст, прерываем выполнение функции
                return None

            self.data = []
            for request_set in data:
                self.data.append({'city': request_set['city'],
                                  'key_words': request_set['key_words'],
                                  'data': [Vacancy().unjsonify(vacancy) for vacancy in request_set['data']]})

    def unload_data(self):
        """Сохраняет обновлённые вакансии"""
        if not self.data:  # если все данные удалены, просто затираем всё в файле data
            with open(self.data_file, 'w', encoding='utf-8') as file:
                pass

        final_list_for_json = []
        for request_set in self.data:
            final_list_for_json.append({'city': request_set['city'],
                                        'key_words': request_set['key_words'],
                                        'data': [vacancy.jsonify() for vacancy in request_set['data']]})
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(final_list_for_json, file, indent=4)

    def add_data(self, city, key_words, data):
        """Добавляет результаты нового поиска"""
        self.data.append({'city': city, 'key_words': key_words, 'data': data})
        self.unload_data()

    def del_data(self, data_set_number):
        """Удаляет результаты поиска по номеру сета"""
        del self.data[data_set_number]
        self.unload_data()

    def get_data(self):
        """Возвращает загруженные данные поиска"""
        return self.data

    def __len__(self):
        return len(self.data)

    def __bool__(self):
        return len(self.data) > 0
