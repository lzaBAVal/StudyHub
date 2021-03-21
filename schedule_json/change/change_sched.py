import json
import re

from datetime import datetime, time
from schedule.output.type_of_sched import WeekDays_EN, WeekDays_RU
from schedule_json.vars import WeekDays_EN, Time, Sched, Lesson, first_lesson


# ----------------------------------------------------------------------------------------------------

def check_input(day: int = None, time_start: str = None, time_end: str = None, name_lesson: str = None,
                teacher: str = None, subgroup: int = None, classroom: str = None):
    if day < 0 or day > 5:
        try:
            raise ValueError('Not valid day!')
        except ValueError:
            print('The day number must be between one and six')
            print('DAY VALUE: ' + str(day))
            return -1, 'Неверно указан день, недели'
    else:
        day -= 1

    if subgroup is None:
        pass
    elif subgroup < 0 or subgroup > 3:
        try:
            raise ValueError('ERROR: Not valid sub_group!')
        except ValueError:
            print('ERROR SUB_GROUP: ' + str(subgroup))
            return -1, 'Неверно указана подгруппа'
    else:
        try:
            raise ValueError('ERROR: Not valid type sub_group!')
        except ValueError:
            print('ERROR SUB_GROUP: ' + str(subgroup))
            return -1, 'Неверно значение подгруппы'
    if name_lesson:
        if re.search(r"['\".<>(){}\]]", name_lesson) or len(name_lesson) > 30:
            try:
                raise ValueError('ERROR: Not valid name_lesson!')
            except ValueError:
                print('ERROR NAME_LESSON: ' + str(name_lesson))
                return -1, 'Имя предмета не должно содержать спец символов и должно быть короче 30 символов'


async def get_free_time(day_of_week: str, sched: dict):
    day_of_week = WeekDays_RU.index(day_of_week)
    if check_input(day_of_week) == -1:
        return -1
    day = WeekDays_EN[day_of_week]
    sched: dict = Sched.parse_obj(sched).dict()
    start, end = [], []
    free_time = []

    if sched[day] is None:
        for t in range(13):
            t_start = time(hour=first_lesson.hour + 1 * t, minute=first_lesson.minute)
            t_end = time(hour=first_lesson.hour + 1 * (t + 1), minute=first_lesson.minute - 20)
            free_time.append(t_start.strftime("%H:%M") + ' - ' + t_end.strftime("%H:%M"))
    else:
        for i in range(len(sched[day]['lessons'])):
            start.append(datetime.strptime(str(sched[day]['lessons'][i]['time']['start']), "%H:%M").time())
            end.append(datetime.strptime(str(sched[day]['lessons'][i]['time']['end']), "%H:%M"))

        for t in range(13):
            t_start = time(hour=first_lesson.hour + 1 * t, minute=first_lesson.minute)
            t_end = time(minute=+60)
            if t_start not in start:
                free_time.append(t_start.strftime("%H:%M") + ' - ' + t_end.strftime("%H:%M"))
    return free_time


def add_lesson(sched, day: int = None, complex_time: str = None, time_start: str = None,
               time_end: str = None, name_lesson: str = None, teacher: str = None,
               subgroup: int = None, classroom: str = None):
    check = check_input(day, time_start, time_end, name_lesson, teacher, subgroup, classroom)
    try:
        if check[0] == -1:
            return check
    except Exception:
        pass

    day = WeekDays_EN[day]
    sched: dict = Sched.parse_obj(sched).dict()

    print(complex_time)

    if complex_time:
        complex_time = re.findall(r'(\d{1,2}[.:]\d{2})[- ]*(\d{1,2}[.:]\d{2})', complex_time)
        ####Добей обработку времени!

    time = {
        "start": time_start,
        "end": time_end
    }
    time = Time(**time)

    lesson = {
        'time': time,
        'subgroup': str(subgroup),
        'lesson': name_lesson,
        'teacher': teacher,
        'classroom': classroom
    }
    lesson = Lesson(**lesson)

    if sched[day] != None:
        for item_lesson in sched[day]['lessons']:
            if item_lesson['time']['start'] == time_start:
                return -1
        sched[day]['lessons'].append(lesson)
    else:
        sched[day] = {'lessons': [lesson]}

    sched = Sched(**sched)
    return sched


def update_lesson(sched, day: int = None, time_start: str = None, time_end: str = None, name_lesson: str = None,
                  teacher: str = None, subgroup: int = None, classroom: str = None):
    check = check_input(day, time_start, time_end, name_lesson, teacher, subgroup, classroom)
    day -= 1
    if check == -1:
        return check

    day = WeekDays_EN[day]
    sched: dict = Sched.parse_raw(sched).dict()

    time = {
        "start": time_start,
        "end": time_end
    }
    time = Time(**time)

    lesson = {
        'time': time,
        'subgroup': str(subgroup),
        'lesson': name_lesson,
        'teacher': teacher,
        'classroom': classroom
    }
    lesson = Lesson(**lesson)

    if sched[day] is not None:
        for l in range(len(sched[day]['lessons'])):
            sched_local = sched[day]['lessons'][l]
            if sched_local['time']['start'] == time_start:
                print('check')
                sched[day]['lessons'][l] = lesson

                sched = Sched(**sched)
                return sched
    return -1


def delete_lesson(sched, day: int = None, time_start: str = None, time_end: str = None, name_lesson: str = None,
                  teacher: str = None, subgroup: int = None, classroom: str = None):
    check = check_input(day, time_start, time_end, name_lesson, teacher, subgroup, classroom)
    day -= 1
    if check == -1:
        return check

    day = WeekDays_EN[day - 1]
    sched: dict = Sched.parse_raw(sched).dict()

    if sched[day] is not None:
        for l in range(len(sched[day]['lessons'])):
            sched_local = sched[day]['lessons'][l]
            if sched_local['time']['start'] == time_start and sched_local['lesson'] == name_lesson \
                    and sched_local['teacher'] == teacher:
                sched[day]['lessons'].pop(l)
                sched = Sched(**sched)
                return sched
    else:
        return -1, 'В этот день нет пар!'


def change_sched_manager():
    pass