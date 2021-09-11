import requests
import time

from core import redis_
from .utils import basic_message_decorator_no_arg
from .markups import generate_start_markup, generate_basic_markup
from ..db.requests import post_help, update_uni, update_year, check_uni, check_year
from ..settings import settings


def day_entered_help(message, date, bot):
    order = redis_.load_data(message.from_user.id)
    order["work_date"] = str(date)
    redis_.dump_data(message.from_user.id, order)

    markup = generate_basic_markup("Пока не известно")
    msg = bot.send_message(
        chat_id=message.from_user.id,
        text=f"Введите время начала работы, пожалуйста:",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_time, bot)


@basic_message_decorator_no_arg
def enter_time(message, bot):
    order = redis_.load_data(message.from_user.id)
    order["work_time"] = str(message.text)
    redis_.dump_data(message.from_user.id, order)

    markup = generate_basic_markup("Пропустить")

    if check_uni(message.chat.id)[0][0] == None:
        msg = bot.send_message(
            chat_id=message.from_user.id,
            text=f"Введите название вашего университета (например: НИУ ВШЭ):",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, enter_uni, bot)
    elif check_year(message.chat.id)[0][0] == None:
        msg = bot.send_message(
            message.chat.id,
            "Введите ваш курс (например: 3 или 1М):",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, enter_year, bot)
    else:
        markup = generate_basic_markup("Не знаю")
        msg = bot.send_message(
            message.chat.id,
            "Введите дисциплину или направление работы (Например: Финансы ):",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, enter_discipline, bot)


@basic_message_decorator_no_arg
def enter_uni(message, bot):
    if message.text == "Пропустить":
        uni = None
    else:
        uni = message.text
        update_uni(uni, message.chat.id)

    if check_year(message.chat.id)[0][0] == None:
        markup = generate_basic_markup("Пропустить")
        msg = bot.send_message(
            message.chat.id,
            "Введите ваш курс (например: 3 или 1М):",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, enter_year, bot)
    else:
        markup = generate_basic_markup("Не знаю")
        msg = bot.send_message(
            message.chat.id,
            "Введите дисциплину или направление работы (Например: Финансы ):",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, enter_discipline, bot)


@basic_message_decorator_no_arg
def enter_year(message, bot):
    if message.text == "Пропустить":
        year = None
    else:
        year = message.text
        update_year(year, message.chat.id)

    markup = generate_basic_markup("Не знаю")

    msg = bot.send_message(
        message.chat.id,
        "Введите дисциплину или направление работы (Например: Финансы ):",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_discipline, bot)


@basic_message_decorator_no_arg
def enter_discipline(message, bot):
    if message.text == "Не знаю":
        discipline = None
    else:
        discipline = message.text

    order = redis_.load_data(message.chat.id)
    order["discipline"] = discipline
    redis_.dump_data(message.chat.id, order)

    markup = generate_basic_markup("Не знаю")

    msg = bot.send_message(
        message.chat.id,
        "Введите формат работы (например: экзамен,кр,тест):",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_format, bot)


@basic_message_decorator_no_arg
def enter_format(message, bot):
    if message.text == "Не знаю":
        format = None
    else:
        format = message.text

    order = redis_.load_data(message.chat.id)
    order["format"] = format
    redis_.dump_data(message.chat.id, order)

    markup = generate_basic_markup("Без комментария")

    msg = bot.send_message(
        message.chat.id,
        "Комментарий к заказу:",
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
    post_help(order)
    redis_.remove_data(message.chat.id)

    markup = generate_start_markup()

    time.sleep(0.3)
    bot.send_message(
        message.chat.id,
        "Скоро админ напишет Вам, ожидайте.",
        reply_markup=markup,
    )

    requests.get(
        f"{settings.admin_url}/order", params={"id": order["id"], "type": "help"}
    )
