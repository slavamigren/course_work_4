from src.parsoperations import JobOperations
from dataoperations import VacancyDataOperations


class UserInterface:
    """Класс с методами для взаимодействия с пользователем"""
    def __init__(self):
        self.api_operations = JobOperations()  # Объект для получения данных с сайтов
        self.v_d_operations = VacancyDataOperations()  # Объект хранения и обработки информации
        self.data_set_number = 0  # Номер запроса из базы данных, с которым сейчас работаем

    def get_city_id_from_api(self):
        """
        Берёт у пользователя название города (или его часть) и верифицирует его с имеющимися на HH и SJ
        или помогает выбрать из похожих
        """
        while True:
            print('По умолчанию поиск производится в Москве, '
                  'для перехода к поиску вакансий в Москве просто нажмите Enter')
            user_city = input('Введите название(или его часть) города: ')
            cities = self.api_operations.get_city(user_city)

            if cities is None:
                print('По Вашему запросу ничего не найдено, попробуйте ещё раз.')
                continue

            if cities[0]:
                print(f'По Вашему запросу найдена локация {cities[1]}.')
                break

            if not cities[0]:
                # если найдено более одного города на каждом ресурсе выбираем из подходящих городов нужный
                found_cities_general_dict = dict(enumerate(cities[1]))
                print('По Вашему запросу найдены следующие города (введите номер нужного города):\n')
                print('\n'.join(f'{n} - {c}' for n, c in found_cities_general_dict.items()))
                while True:
                    city_number = input()
                    if not city_number.isdigit() or int(city_number) < 0 or int(city_number) > len(
                            found_cities_general_dict):
                        print('Введите номер одного из найденных городов\n')
                    else:
                        final_city = found_cities_general_dict[int(city_number)]
                        self.api_operations.get_city(final_city)
                        break
                break

    def load_vacancies_from_api(self):
        """Загружает по ключевому слову вакансии и сохраняет в VacancyDataOperations"""
        print('Введите ключевые слова для поиска вакансии:')
        key_words = input()
        print('Идёт загрузка информации с НН и SJ, ожидание примерно 20 секунд...')
        vacancies = self.api_operations.load_vacancies(key_words)
        if not len(vacancies):
            print(f"Найдено 0 вакансий")
            return False
        self.v_d_operations.add_data(self.api_operations.city_name, self.api_operations.key_words, vacancies)

    def get_new_vacancy(self):
        """
        Весь процесс взаимодействия с пользователем для отправки нового запроса на
        HH и SJ и сохранения в VacancyDataOperations
        """
        self.get_city_id_from_api()
        if not self.load_vacancies_from_api():
            return False
        self.data_set_number = -1

    def data_set_choice(self):
        """Выбор данных из сохранённых запросов"""
        print('Доступны сохранённые вакансии из запросов:')
        for i in range(len(self.v_d_operations.data)):
            print(f"{i}: город {self.v_d_operations.data[i]['city']}, "
                  f"запрос: {self.v_d_operations.data[i]['key_words']}")
        print()

        while True:
            print('Введите номер запроса:')
            req_num = input()
            if not req_num.isdigit() or int(req_num) < 0 or int(req_num) >= len(self.v_d_operations.data):
                print('должен быть введён номер из предложенных')
                continue
            else:
                self.data_set_number = int(req_num)
                break

    def sort_and_show(self):
        print(f"Найдено {len(self.v_d_operations.data[self.data_set_number]['data'])} вакансий")
        print('Хотите отсортировать вакансии по зарплате?')
        sort = self.choose_one({0: 'не сортировать', 1: 'по возрастанию', 2: 'по убыванию'})
        if sort == 1:
            self.v_d_operations.data[self.data_set_number]['data'].sort()
        elif sort == 2:
            self.v_d_operations.data[self.data_set_number]['data'].sort(reverse=True)

        print('Хотите просмотреть топ 10 вакансий в соответствии с сортировкой'
              'или будете смотреть постранично (по 10 вакансий)?')
        top = self.choose_one({0: 'показать топ', 1: 'смотреть постранично'})
        print()
        print('------------------------------начало просмотра------------------------------')
        print()
        if top == 0:
            for vacancy in self.v_d_operations.data[self.data_set_number]['data'][:10]:
                print(vacancy)
                print()
                print('------------------------------следующая вакансия------------------------------')
                print()
        else:
            cnt = 0
            for i in range(len(self.v_d_operations.data[self.data_set_number]['data'])):
                print(self.v_d_operations.data[self.data_set_number]['data'][i])
                print()
                print('------------------------------следующая вакансия------------------------------')
                print()
                cnt += 1
                if cnt == 10:
                    print('для просмотра следующей страницы нажмите Enter, '
                          'для прекращения просмотра нажмите Пробел и Enter')
                    if input() == ' ':
                        break
                    else:
                        cnt = 0
                if i == len(self.v_d_operations.data[self.data_set_number]['data']) - 1:
                    print('просмотр закончен')

    def del_set_of_data(self):
        print('Вы точно хотите удалить выбранный запрос из базы данных?\n')
        if self.choose_one({0: 'отмена', 1: 'удаление'}):
            self.v_d_operations.del_data(self.data_set_number)

    @staticmethod
    def choose_one(choose_dict):
        """Возвращает выбор пользователя из предложенных в словаре {1: 'вариант-1', 2: 'вариант-2',..}"""
        while True:
            print(", ".join((" - ".join((str(n), q)) for n, q in choose_dict.items())))
            position = input()
            if not position.isdigit() or int(position) < min(choose_dict) or int(position) > max(choose_dict):
                print('должен быть введён номер из предложенных')
                continue
            else:
                return int(position)


"""
if __name__ == '__main__':
    user_session = UserInterface()
    print('Привет!')

    while True:
        if user_session.v_d_operations:
            print('В базе данных есть результаты предыдущих поисков, '
                  'хотите посмотреть, сделаете новый запрос на работные сайты или выйти из программы?')
            num = user_session.choose_one({0: 'посмотреть, что есть в базе',
                                           1: 'сделать новый поиск на работных сайтах',
                                           2: 'выйти из программы'})
        else:
            print('В базе данных нет результатов предыдущих поисков, '
                  'хотите сделать новый запрос на работные сайты или выйти из программы?')
            num = user_session.choose_one({1: 'сделать новый поиск на работных сайтах',
                                           2: 'выйти из программы'})
        if num == 2:
            quit()
        elif num == 1:
            search = 1
            while not user_session.get_new_vacancy():
                print('Хотите поискать ещё?')
                search = user_session.choose_one({0: 'не продолжать поиск', 1: 'попробовать ещё раз'})
                if not search:
                    break
            if search != 0:
                user_session.sort_and_show()
        else:
            user_session.data_set_choice()
            print('Хотите просмотреть или удалить выбранный запрос?')
            num = user_session.choose_one({0: 'просмотреть', 1: 'удалить'})
            if not num:
                user_session.sort_and_show()
            else:
                user_session.del_set_of_data()

"""