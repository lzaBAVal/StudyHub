state_change_success_message = 'Текущее состояние успешно изменено'
state_reset_message = 'Состояние успешно сброшено'
current_state_message = 'Текущее состояние - "{current_state}", что удовлетворяет условию "один из {states}"'

calc_error = 'Произошла ошибка при расчете оценки. Пожалуйста проверьте еще раз оценки которые вы вводите. В случае ' \
             'если вы считаете, что вводите все верно, сообщите об этом случае админу.'
calc_one_result = 'Для желаемой итоговой оценки на экзамене вам необходимо' \
                  'получить "{0}"\nУдачи!'
calc_many_result = 'Для получения {0} баллов нужно получить {1}'
calc_many_result_reuse = 'Для {0} - {1}'

wtf_error = 'Что-то произошло, о проблеме пиши админу!'

start_text = \
    "Привет, студент! Я бот, который постарается помочь тебе в учебных процесах " \
    "\nНа данный момент идет тестовый период моей работы." \
    "\nЯ могу ошибаться, тормозить в общем работать не так как нужно)" \
    "\nЕсли ты хочешь пользоваться моим функционалом или помочь то Welcome :D" \
    "\nРазработчик будет очень рад если ты будешь отправлять ему замечания по поводу моей работы!"

help_user_text = \
    '/id - выведет ваш chat_id который вам выдал телеграм\n' \
    '/bio - выведет информацию о вас: имя, фамилия, группа, дата регистрации, ваш статус\n' \
    '/classmates - выводит список студентов состоящих в вашей группе\n' \
    '/deleteme - удаляет ваш аккаунт из бота. Внимание все данные удаляться вместе с вашим личным расписание\n'

cant_show_schedule_str = 'Не удалось показать расписание, сообщите об этом админу.'

help_anon_str = '/check - С помощью данной команды можно проверить есть ли вы в базе.' \
                '\nДанной командой логично воспользваоться в случае если произошел сбой в логике бота и ' \
                'вы стали неизвестным для бота. ' \
                '\nЗлоупотреблять данной командой не стоит'

help_admin_str = (
        '/cancel_func - отменяет текущий процесс операции\n'
        '/id - выведет ваш chat_id который вам выдал телеграм\n'
        '/bio - выведет информацию о вас: имя, фамилия, группа, дата регистрации, ваш статус\n'
        '/group_info - выведет информацию о вашей группе, имя старосты, количество человек в состоящих в группе и '
        'пользующихся ботом\n '
        '/check_user_bio - показывает информацию о пользователе чей id вы введете\n'
        '/users_list - выводит список студентов с их именем, группой, id\n'
        '/give_rights - выдать права старосты студенту\n'
        '/take_away_rights - забрать права старосты у студента\n'
        '/add_hash - добавляет в базу новый ключ для старосты\n'
        '/get_free_hashes - вывести список свободных ключей\n'
        '/last_logs - бот отправит все самые свежие логи (не больше 3000 символов) в одном сообщении\n'
        '/last_critical - выведет последние несколько записей логов уровня ERROR, WARNING, CRITICAL\n'
        '/print_arhit или /print_group - выведет расписание определнной группы в необработанном виде '
        '(нужно для дебага)\n'
        ''
)

help_captain_str = (
    '/lock_group - закрывает вход в группу для новых студентов, данная настройка нужна для того чтобы посторонние '
    'не могли смотреть что у вас есть\n'
    '/unlock_group - открывает вход в группу всем желающим при регистрации. Не стоит держать группу открытой, '
    'используйте настройку с умом\n'
    '/group_info - выводит информацию о вашей группе: кто состоит в вашей группе, настройки группы.'
)


def calc_output(rating) -> str:
    if rating == -1:
        return calc_error
    elif type(rating) == float:
        return calc_one_result.format(rating)
    elif type(rating) == tuple:
        target = rating[0]
        rating = rating[1]
        res = []
        for i in range(len(rating)):
            if i == 0:
                res.append((calc_many_result.format(target[i], rating[i])))
            else:
                res.append((calc_many_result_reuse.format(target[i], rating[i])))
        return "\n".join(res)
    else:
        return wtf_error


def inaccessible_variants_output(variants):
    excluded = []
    taken = []
    sep = ' ,'
    result = ''
    for i in variants:
        if variants[i] == 'excluded':
            excluded.append(i)
        else:
            taken.append(f'{i}')
    if excluded:
        result += f'Варианты которые брать нельзя: {sep.join(map(str, excluded))}.'
    if taken:
        result += f'\nЗанятые варианты: {sep.join(map(str, taken))}.'
    return result


def taken_variants_output(variants):
    taken = []
    sep = ' ,'
    result = ''
    for i in variants:
        if variants[i] != 'excluded':
            taken.append(f'{i}')
    if taken:
        result += f'\nЗанятые варианты: {sep.join(map(str, taken))}.'
    return result
