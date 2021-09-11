import requests
import time

from core import redis_
from .utils import calendar_markup, basic_message_decorator_no_arg, cancel_order
from .markups import generate_start_markup, generate_basic_markup
from ..db.requests import post_work, update_uni, update_year, check_uni, check_year
from ..settings import settings
from .filer import download_file


@basic_message_decorator_no_arg
def enter_type(message, bot):
    if message.text == "Другое (Ввести вручную)":
        msg = bot.send_message(
            message.chat.id,
            "Введите собственный тип работы:",
        )
        bot.register_next_step_handler(msg, enter_another_type, bot)
    else:
        order = redis_.load_data(message.chat.id)
        order["order_type"] = message.text
        redis_.dump_data(message.chat.id, order)

        calendar_markup(
            message, bot, "Укажите день, к которому работа должна быть выполнена"
        )


@basic_message_decorator_no_arg
def enter_another_type(message, bot):
    order = redis_.load_data(message.chat.id)
    order["order_type"] = message.text
    redis_.dump_data(message.chat.id, order)

    calendar_markup(
        message, bot, "Укажите день, к которому работа должна быть выполнена"
    )


def day_entered_work(message, date, bot):
    order = redis_.load_data(message.from_user.id)
    order["work_date"] = str(date)
    redis_.dump_data(message.from_user.id, order)

    markup = generate_basic_markup("Пропустить")

    if check_uni(message.from_user.id)[0][0] == None:
        msg = bot.send_message(
            chat_id=message.from_user.id,
            text=f"Введите название вашего университета (например: НИУ ВШЭ):",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, enter_uni, bot)
    elif check_year(message.from_user.id)[0][0] == None:
        msg = bot.send_message(
            message.from_user.id,
            "Введите ваш курс (например: 3 или 1М):",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, enter_year, bot)
    else:
        markup = generate_basic_markup("Не знаю")
        msg = bot.send_message(
            message.from_user.id,
            "Введите дисциплину работы (например: Финансы):",
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
            "Введите дисциплину работы (например: Финансы):",
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
        "Введите дисциплину работы (например: Финансы):",
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
        "Введите тему работы:",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_theme, bot)


@basic_message_decorator_no_arg
def enter_theme(message, bot):
    if message.text == "Не знаю":
        theme = None
    else:
        theme = message.text

    order = redis_.load_data(message.chat.id)
    order["theme"] = theme
    redis_.dump_data(message.chat.id, order)

    markup = generate_basic_markup("Не знаю")
    if order["order_type"] == "Презентация":
        text_message = "Введите обьем презентации (например: 10 слайдов):"
    elif order["order_type"] == "Докторская":
        text_message = "Введите обьем докторской (например: 200 стр):"
    elif order["order_type"] == "Кандидатская":
        text_message = "Введите обьем кандидатской (например: 150 стр):"
    elif order["order_type"] == "МВА":
        text_message = "Введите обьем работы (например: 100 стр):"
    elif order["order_type"] == "Дипломная":
        text_message = "Введите обьем диплома (например: 60 стр):"
    elif order["order_type"] == "Реферат":
        text_message = "Введите обьем реферата (например: 15-20 стр):"
    elif order["order_type"] == "Эссе":
        text_message = "Введите обьем эссе (например: 10-15 стр):"
    elif order["order_type"] == "Курсовая":
        text_message = "Введите обьем курсовой (например: 25-30 стр):"
    else:
        text_message = "Введите обьем работы (например: 20 стр):"

    msg = bot.send_message(
        message.chat.id,
        text_message,
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_volume, bot)


@basic_message_decorator_no_arg
def enter_volume(message, bot):
    try:
        volume = int(message.text)
    except:
        volume = None

    order = redis_.load_data(message.chat.id)
    order["volume"] = volume
    redis_.dump_data(message.chat.id, order)

    markup = generate_basic_markup("Не знаю")

    msg = bot.send_message(
        message.chat.id,
        "Введите процент оригинальности, (например: 85%+):",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_unique_persentage, bot)


@basic_message_decorator_no_arg
def enter_unique_persentage(message, bot):
    try:
        if len(message.text) == 1 or len(message.text) == 2:
            persentage = int(message.text)
        else:
            persentage = int(message.text[:2])
    except:
        persentage = None

    order = redis_.load_data(message.chat.id)
    order["unique_persentage"] = persentage
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
    order["file_names"] = []
    redis_.dump_data(message.chat.id, order)

    markup = generate_basic_markup("Подтвердить заказ")

    bot.send_message(
        message.chat.id,
        "Прикрепите файл, если нужно",
    )
    msg = bot.send_message(
        message.chat.id,
        'Подсказка: "Откройте файл в любом сторонним приложении, нажмите Отправить -> Telegram -> Pomosh4 Student"',
        reply_markup=markup,
    )
    counter = 0
    bot.register_next_step_handler(msg, enter_file, bot, counter)


def ask_for_file(message, bot, counter):
    markup = generate_basic_markup("Подтвердить заказ")

    bot.send_message(
        message.chat.id,
        "Прикрепите еще файл, если нужно",
    )
    msg = bot.send_message(
        message.chat.id,
        'Подсказка: "Откройте файл в любом сторонним приложении, нажмите Отправить -> Telegram -> Pomosh4 Student"',
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_file, bot, counter)


def enter_file(message, bot, counter):
    if message.text == "Отмена" or message.text == "Назад":
        cancel_order(message, bot)
    elif message.text == "Подтвердить заказ":
        time.sleep(0.3)
        finish(message, bot)
    else:
        counter += 1
        file_name = download_file(message, bot)

        order = redis_.load_data(message.chat.id)
        order["file_names"].append(file_name)
        redis_.dump_data(message.chat.id, order)

        if counter < 5:
            ask_for_file(message, bot, counter)
        else:
            bot.send_message(
                message.chat.id,
                "Больше файлов прикреплять нельзя.",
            )
            time.sleep(0.3)
            finish(message, bot)


def finish(message, bot):
    order = redis_.load_data(message.chat.id)
    post_work(order)
    redis_.remove_data(message.chat.id)

    markup = generate_start_markup()

    bot.send_message(
        message.chat.id,
        "Скоро админ напишет Вам, ожидайте.",
        reply_markup=markup,
    )

    try:
        requests.get(
            f"{settings.admin_url}/order", params={"id": order["id"], "type": "work"}
        )
    except:
        bot.send_message(
            message.chat.id,
            "Произошла какая-то ошибка с сервером, пожалуйста подождите немного и повторите Ваш заказ.",
            reply_markup=markup,
        )
