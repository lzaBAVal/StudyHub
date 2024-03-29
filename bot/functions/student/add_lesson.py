import re

from aiogram import types
from aiogram.dispatcher import FSMContext

import bot.keyboard.keyboard as kb
from DB.models import Student
from bot.functions.student.flexible_time import check_flex_time
from bot.functions.whois import whois
from bot.schedule.change.change_sched import get_free_time, add_lesson, check_busy_time
from bot.schedule.output.get_schedule_object import get_sched, update_sched
from bot.states.states import AddLesson
from bot.vars import WeekDays_RU, special_chars, special_chars_digit
from log.logging_core import init_logger

logger = init_logger()


async def add_lesson_time(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if message.text.lower() not in WeekDays_RU:
            await message.answer(text='Введите день недели!', reply_markup=kb.days())
            return 0
        try:
            whose = await whois(message)
        except Exception as exc:
            logger.exception(exc)
            return -1
        sched = await get_sched(message.chat.id, whose)
        free_time = await get_free_time(message.text.lower(), sched)
        async with state.proxy() as data:
            data['day'] = message.text.lower()
            data['sched'] = sched
            data['free_time'] = free_time
    data = await state.get_data()
    await message.answer(text='Введите время на которое хотите назначить урок. '
                              'Вы можете выбрать время которое представлено ниже либо ввести его самому .'
                              'Если вы хотите ввести свое время, формат сообщения должен быть таким:\n'
                              '12:15 - 14:40',
                         reply_markup=kb.free_time(data['free_time']))
    await AddLesson.next()


async def add_lesson_lesson(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        async with state.proxy() as data:
            pass
        if not check_flex_time(message.text):
            await message.answer(text='Введите время на которое хотите назначить урок. '
                                      'Вы можете выбрать время которое представлено ниже либо ввести его самому .'
                                      'Если вы хотите ввести свое время формат сообщения должен быть таким:\n'
                                      '\t12:15 - 14:40',
                                 reply_markup=kb.free_time(data['free_time']))
            await AddLesson.time.set()
            return False

        if await check_busy_time(message.text, data['sched'], data['day']):
            await message.answer('Указанное время уже занято')
            return False

        async with state.proxy() as data:
            data['time'] = message.text
    await message.answer('Введите название урока')
    await AddLesson.next()


async def add_lesson_teacher(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if len(message.text) <= 30 and not re.match(special_chars, message.text):
            async with state.proxy() as data:
                data['lesson'] = message.text
        else:
            await message.answer(text='Название урока должно быть меньше 30 символов и состоять только из букв и цифр!')
            await AddLesson.lesson.set()
            return 0
    await message.answer('Введите имя преподавателя')
    await AddLesson.next()


async def add_lesson_subgroup(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if len(message.text) <= 30 and not re.match(special_chars_digit, message.text):
            async with state.proxy() as data:
                data['teacher'] = message.text
        else:
            await message.answer(text='Имя преподавателя должно быть меньше 30 символов и состоять только из букв!')
            await AddLesson.teacher.set()
            return 0
    await message.answer('Введите подгруппу', reply_markup=kb.subgroup_kb)
    await AddLesson.next()


async def add_lesson_classroom(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if message.text.lower() == 'нет подгрупп' and not re.match(special_chars, message.text) or \
                re.match(r'\d', message.text):
            async with state.proxy() as data:
                data['subgroup'] = message.text
        else:
            await message.answer(text='Введите либо номер подгруппы либо укажите что подгрупп нет')
            await AddLesson.subgroup.set()
            return 0
    await message.answer('Введите номер кабинета или укажите что вы учитесь онлайн', reply_markup=kb.classroom_kb)
    await AddLesson.next()


async def add_lesson_check(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if len(message.text) <= 10 and not re.match(special_chars, message.text) or \
                message.text.lower() == 'онлайн':
            async with state.proxy() as data:
                data['classroom'] = message.text
            await message.answer(
                f"Проверьте данные: \n"
                f"День: {data['day']}\n\t"
                f"Время: {data['time']}\n\t"
                f"Урок: {data['lesson']}\n\t"
                f"Преподаватель: {data['teacher']}\n\t"
                f"Подгруппа: {data['subgroup']}\n\t"
                f"Кабинет: {data['classroom']}\n\n"
                f"Все верно?",
                reply_markup=kb.question_kb)
        else:
            await message.answer(
                text='Требуется наименование кабинет. Длина не более 10 символов или укажите что вы учитесь онлайн')
            await AddLesson.classroom.set()
            return 0

    await AddLesson.next()


async def add_lesson_process(message: types.message, state: FSMContext):
    data = await state.get_data()
    try:
        sched = await add_lesson(sched=data['sched'], day=WeekDays_RU.index(data['day']), complex_time=data['time'],
                                 classroom=data['classroom'], name_lesson=data['lesson'], teacher=data['teacher'])
        whose_schedule = await Student.filter(chat_id=message.chat.id).values_list('whose_schedule')
        whose_schedule = whose_schedule[0][0]
        print(f'whose_schedule = whose_schedule[0][0] {whose_schedule}')
        await update_sched(message.chat.id, sched, whose_schedule)
        await AddLesson.next()
        await message.answer('Идет процесс занесения урока в базу! Для завершения тыкните на котика',
                             reply_markup=kb.cat_kb)
    except Exception as exc:
        logger.exception(exc)
        await message.answer('При добавлении предмета в расписание произошла ошибка.')
        return 1
