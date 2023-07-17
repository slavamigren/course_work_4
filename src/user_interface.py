from src.Operations import JobOperations
import json

class UserInterface:

    def __init__(self):
        self.joboperations = JobOperations()  # все операции с данными выполняются в этом объекте

    def get_city_id(self):
        """
        Берёт у пользователя название города (или его часть) и верифицирует его с имеющимися на HH и SJ
        или помогает выбрать из похожих
        """
        while True:
            print('По умолчанию поиск производится в Москве, для перехода к поиску вакансий в Москве просто нажмите Enter')
            user_city = input('Введите название(или его часть) города: ')
            cities = self.joboperations.get_city(user_city)

            if cities is None:
                print('По Вашему запросу ничего не найдено, попробуйте ещё раз.')
                continue

            if cities[0]:
                print(f'По Вашему запросу найдена локация {cities[1]}.')
                break

            if not cities[0]:
                # если найдено более одного города на каждом ресурсе выбираем из подходящих городов нужный
                found_cities_general_dict = dict(enumerate(cities[1]))
                print('По Вашему запросу найдены следующие города (введите номер нужного города)\n',
                      '(выход - чтобы выйти, повторить - чтобы повторить ввод названия города):')
                print('\n'.join(f'{n} - {c}' for n, c in found_cities_general_dict.items()))
                while True:
                    city_number = input()
                    if city_number.lower() == 'выход':
                        return None
                    if city_number.lower() == 'повторить':
                        break
                    if not city_number.isdigit() or int(city_number) < 0 or int(city_number) > len(
                            found_cities_general_dict):
                        print('Введите номер одного из найденных городов\n',
                              '(выход - чтобы выйти, повторить - чтобы повторить ввод названия города):')
                    else:
                        final_city = found_cities_general_dict[int(city_number)]
                        cities = self.joboperations.get_city(final_city)
                        print(f'По Вашему запросу найдена локация {cities[1]}.')

    def load_vacancies(self):
        print('Введите ключевые слова для поиска вакансии:')
        self.joboperations.get_key_words(input())
        print('идёт загрузка информации с НН и SJ, ожидание примерно 10 секунд...')
        self.joboperations.load_vacancies()
        #print(f' Найдено {len(self.joboperations.vacancies)} вакансий')


if __name__ == '__main__':
    a = UserInterface()
    a.get_city_id()
    a.load_vacancies()
    #for i in range(10):
    #    print(a.joboperations.vacancies[i])
    #    print('----------------------------------------------------------------')

