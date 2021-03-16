from aiogram.types import ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup

all_shedule_btn = KeyboardButton("Все расписание")
next_lesson_btn = KeyboardButton("Cледующая пара")
todays_shedule_btn = KeyboardButton("Расписание на сегодня")
rating_btn = KeyboardButton("Расчитать итоговую оценку")
alert_btn = KeyboardButton("Настройка уведомлений")
find_group_btn = KeyboardButton("Найти группу")
register_btn = KeyboardButton("Регистрация")
register_cancel = KeyboardButton("Отменить регистрацию")
register_yes = KeyboardButton("Да")
register_no = KeyboardButton("Нет")

keys_btn = KeyboardButton("У меня есть ключ")

cat = '🐈'

stud_kb = ReplyKeyboardMarkup(resize_keyboard=True)
stud_kb.row(all_shedule_btn, next_lesson_btn, todays_shedule_btn)
stud_kb.add(rating_btn, find_group_btn)
stud_kb.row(alert_btn)

tester_kb = ReplyKeyboardMarkup(resize_keyboard=True)
tester_kb.add(keys_btn)

anon_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
anon_kb.row(register_btn)

question_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
question_kb.row(register_yes, register_no)

register_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
register_kb.add(register_cancel)

cat_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cat_kb.row(cat)


def createButtons(btns_l: list):
    group = []
    for i in btns_l:
        group.append(i)
    test = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(group)):
        if i % 2 == 0:
            test.row(KeyboardButton(str(group[i])))
        else:
            test.add(KeyboardButton(str(group[i])))
        test.add(register_cancel)
    return test


# greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_hi)

# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)