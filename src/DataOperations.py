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
    def del_data(self):
        pass

class VacancyDataOperations(DataOperations):

    FILE = 'data.json'

    def __init__(self):
        self.data = []
        self.load_data()

    def load_data(self):
        with open(self.FILE, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except:  # если файл пуст, прерываем выполнение функции
                return None

            self.data = []
            for set in data:
                self.data.append({'city': set['city'],
                                            'key_words': set['key_words'],
                                            'data': [Vacancy().unjsonify(vacancy) for vacancy in set['data']]})

    def unload_data(self):
        if not self.data:  # если все данные удалены, просто затираем всё в файле data
            with open(self.FILE, 'w', encoding='utf-8') as file:
                pass

        final_list_for_json = []
        for set in self.data:
            final_list_for_json.append({'city': set['city'],
                                        'key_words': set['key_words'],
                                        'data': [vacancy.jsonify() for vacancy in set['data']]})
        with open(self.FILE, 'w', encoding='utf-8') as file:
            json.dump(final_list_for_json, file, indent=4)

    def add_data(self, city, key_words, data):
        self.data.append({'city': city, 'key_words': key_words, 'data': data})
        self.unload_data()

    def del_data(self, city=None, key_words=None):
        del_num = None
        if city:
            del_key, del_volume = 'city', city
        else:
            del_key, del_volume = 'key_words', key_words
        for set_num in range(len(self.data)):
            if self.data[set_num][del_key] == del_volume:
                del_num = set_num
                break
        if del_num:
            del self.data[del_num]
            self.unload_data()
            return True
        return False


    def get_data(self):
        return self.data

#if __name__ == '__main__':
