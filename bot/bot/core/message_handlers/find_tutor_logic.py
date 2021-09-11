import requests
import time

from core import redis_
from .utils import basic_message_decorator_no_arg
from .markups import (
    generate_basic_markup,
    generate_tutor_sex_makup,
    generate_start_markup,
)
from ..db.requests import post_tutor
from ..settings import settings


@basic_message_decorator_no_arg
def enter_study_type(message, bot):
    study_type = message.text[2:]
    order = redis_.load_data(message.chat.id)
    order["study_type"] = study_type
    redis_.dump_data(message.chat.id, order)

    markup = generate_basic_markup("Не знаю")

    if study_type == "Школа":
        order = redis_.load_data(message.chat.id)
        order["study_name"] = None
        redis_.dump_data(message.chat.id, order)

        msg = bot.send_message(
            message.chat.id,
            "Укажите класс:",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, enter_study_year, bot)
    else:
        msg = bot.send_message(
            message.chat.id,
            "Введите название учебного заведения:",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, enter_study_name, bot)


@basic_message_decorator_no_arg
def enter_study_name(message, bot):
    if message.text == "Не знаю":
        study_name = None
    else:
        study_name = message.text

    order = redis_.load_data(message.chat.id)
    order["study_name"] = study_name
    redis_.dump_data(message.chat.id, order)

    markup = generate_basic_markup("Не знаю")

    msg = bot.send_message(
        message.chat.id,
        "Укажите курс:",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_study_year, bot)


@basic_message_decorator_no_arg
def enter_study_year(message, bot):
    if message.text == "Не знаю":
        study_year = None
    else:
        study_year = message.text

    order = redis_.load_data(message.chat.id)
    order["study_year"] = study_year
    redis_.dump_data(message.chat.id, order)

    markup = generate_basic_markup("Не знаю")

    msg = bot.send_message(
        message.chat.id,
        "Укажите предмет (предметы) по которым необходима помощь:",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_lessons, bot)


@basic_message_decorator_no_arg
def enter_lessons(message, bot):
    if message.text == "Не знаю":
        lessons = None
    else:
        lessons = message.text

    order = redis_.load_data(message.chat.id)
    order["lessons"] = lessons
    redis_.dump_data(message.chat.id, order)

    markup = generate_tutor_sex_makup()

    msg = bot.send_message(
        message.chat.id,
        "Укажите желаемый пол преподавателя:",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_tutor_sex, bot)


@basic_message_decorator_no_arg
def enter_tutor_sex(message, bot):
    if message.text == "Не важно":
        tutor_sex = None
    else:
        tutor_sex = message.text

    order = redis_.load_data(message.chat.id)
    order["tutor_sex"] = tutor_sex
    redis_.dump_data(message.chat.id, order)

    markup = generate_basic_markup("Без комментария")

    msg = bot.send_message(
        message.chat.id,
        "Комментарий (укажите к чему хотите подготовиться и прочие пожелания):",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_comment, bot)


@basic_message_decorator_no_arg
def enter_comment(message, bot):
    if message.text == "Без комментария":
        comment = None
    else:
        comment = message.text

    order = redis_.load_data(message.chat.id)
    order["comment"] = comment
    post_tutor(order)
    redis_.remove_data(message.chat.id)

    markup = generate_start_markup()

    time.sleep(0.3)
    bot.send_message(
        message.chat.id,
        "Скоро админ напишет Вам, ожидайте.",
        reply_markup=markup,
    )

    requests.get(
        f"{settings.admin_url}/order", params={"id": order["id"], "type": "tutor"}
    )
