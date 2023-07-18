from userinterface import UserInterface

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
        break
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