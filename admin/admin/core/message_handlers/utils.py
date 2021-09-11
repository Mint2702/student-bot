from loguru import logger
from datetime import datetime

from ..db.requests import check_user


def auth(bot):
    def dec(func):
        def wrapper(message, *args, **kwargs):
            if check_user(message.chat.id):
                try:
                    func(message, *args, **kwargs)
                except Exception as err:
                    logger.error("Some error occured while handling message.")
                    logger.warning(err)
            else:
                bot.send_message(
                    message.chat.id,
                    f"Пожалуйста авторизуйтесь с помощью команды '/start'",
                )

        return wrapper

    return dec


def reformat_date(date: str) -> str:
    new_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%y")
    return new_date


def format_work(order: dict) -> str:
    result = f'Заказ работы:\nВУЗ: {order["uni"]}\nКурс: {order["study_year"]}\nТип работы: {order["order_type"]}\nДисциплина: {order["discipline"]}\nТема: {order["theme"]}\nОригинальность: {order["unique_persentage"]}\nОбьем: {order["volume"]}\nДата сдачи: {reformat_date(order["work_date"][:-9])}\nКомментарий: {order["comment"]}\nЗаказчик: {order["first_name"]}\n\nНик: @{order["username"]}\nЗаказчик: {order["first_name"]}\nФамилия: {order["last_name"]}'
    return result


def format_help(order: dict) -> str:
    result = f'Заказ онлайн помощи:\nВУЗ: {order["uni"]}\nКурс: {order["study_year"]}\nДата: {reformat_date(order["work_date"][:-9])}\nДисциплина: {order["discipline"]}\nФормат: {order["format"]}\nВремя работы: {order["work_time"]}\nКомментарий: {order["comment"]}\n\nНик: @{order["username"]}\nИмя: {order["first_name"]}\nФамилия: {order["last_name"]}'
    return result


def format_tutoring(order: dict) -> str:
    if order["study_type"] == "Школа":
        result = f'Заказ репетиторства:\nМесто обучения: {order["study_type"]}\nКласс: {order["study_year"]}\nПредмет(ы): {order["lessons"]}\nПол преподавателя: {order["tutor_sex"]}\nКомментарий: {order["comment"]}\n\nНик: @{order["username"]}\nИмя: {order["first_name"]}\nФамилия: {order["last_name"]}'
    else:
        result = f'Заказ репетиторства:\nМесто обучения: {order["study_type"]}\nНазвание учебного заведения: {order["study_name"]}\nКурс: {order["study_year"]}\nПредмет(ы): {order["lessons"]}\nПол преподавателя: {order["tutor_sex"]}\nКомментарий: {order["comment"]}\n\nНик: @{order["username"]}\nИмя: {order["first_name"]}\nФамилия: {order["last_name"]}'
    return result


def format_stat(works: list, helps: list, type_stat: str) -> str:
    works = [dict(work) for work in works]
    helps = [dict(help) for help in helps]

    res_dict_works = {}
    res_dict_helps = {}

    for work in works:
        type = work["order_type"]
        if res_dict_works.get(type, False):
            res_dict_works[type] += 1
        else:
            res_dict_works[type] = 1

    for help in helps:
        type = help["format"]
        if res_dict_helps.get(type, False):
            res_dict_helps[type] += 1
        else:
            res_dict_helps[type] = 1

    if type_stat == "month":
        intro = "За последний месяц было заказано:"
    elif type_stat == "year":
        intro = "За последний год было заказано:"
    else:
        intro = "За все время было заказано:"

    stat = f"{intro}\n  Работ:\n"
    for item in res_dict_works.items():
        stat += f"    {item[0]}  -  {item[1]}\n"

    stat += "\n  Помощи онлайн:\n"
    for item in res_dict_helps.items():
        stat += f"    {item[0]}  -  {item[1]}\n"

    return stat
