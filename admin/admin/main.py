from flask import Flask, request
from telebot import TeleBot
import threading
import time
from pathlib import Path

from core.settings import settings
from core.db.requests import (
    get_user,
    commit_user,
    get_help,
    get_work,
    get_admins,
    get_works,
    get_helps,
    get_users_num,
    get_tutoring,
)
from core.message_handlers.utils import (
    auth,
    format_work,
    format_help,
    format_stat,
    format_tutoring,
)
from core.message_handlers.markups import generate_markup


TOKEN = settings.token
bot = TeleBot(TOKEN, parse_mode=None)

app = Flask(__name__)


@bot.message_handler(commands=["start"])
def start(message):
    msg = bot.send_message(
        message.chat.id,
        f"Приветствуем, {message.from_user.first_name}! Введи пароль админа:",
    )
    bot.register_next_step_handler(msg, enter_password)


def enter_password(message):
    user = get_user(message.chat.id)
    if message.text == settings.password and user != []:
        commit_user(message.chat.id)
        markup = generate_markup()
        bot.send_message(
            message.chat.id,
            "Вы авторизованы в качестве администратора",
            reply_markup=markup,
        )
    else:
        bot.send_message(
            message.chat.id,
            "Неверный пароль или вы не зарегестрированы на основном боте",
        )


@bot.message_handler(regexp="пользователей")
@auth(bot)
def users_num(message):
    users = get_users_num()[0][0]
    msg = bot.send_message(
        message.chat.id,
        f"Количество пользователей - {users}",
    )


@bot.message_handler(regexp="стат")
@auth(bot)
def stat(message):
    msg = "Введите дату начала и конца интересующего вас отрезка в формате - '2021-06-31 2021-12-31'"
    msg = bot.send_message(
        message.chat.id,
        msg,
    )
    bot.register_next_step_handler(msg, enter_dates_for_stat)


def enter_dates_for_stat(message):
    dates = message.text.strip().split(" ")
    try:
        start = dates[0]
        end = dates[1]
        works = get_works(start, end)
        helps = get_helps(start, end)
        stat = format_stat(works, helps, "all")
    except:
        stat = "Вы ввели даты не в том формате, попробуйте еще раз, пожалуйста."

    bot.send_message(
        message.chat.id,
        stat,
    )


@bot.message_handler(func=lambda m: True)
@auth(bot)
def echo_all(message):
    bot.reply_to(message, "Вы авторизованы, но ваш запрос не понятен боту...")


@app.route("/order")
def order():
    type = request.args.get("type")
    id = request.args.get("id")

    admins = get_admins()

    if len(admins) == 0:
        return "No admins"

    if type == "work":
        order = dict(get_work(id))
        message = format_work(order)
    elif type == "help":
        order = dict(get_help(id))
        message = format_help(order)
    else:
        order = dict(get_tutoring(id))
        message = format_tutoring(order)

    for id in admins:
        id = id[0]
        bot.send_message(
            id,
            message,
        )
        file_names = order.get("file_names", False)
        if file_names:
            for file_name in file_names:
                cur_path = str(Path("../bot_files").absolute())
                print(cur_path)
                extencion = file_name[-3:]
                user_id = order["user_id"]

                markup = generate_markup()

                if extencion == "jpg":
                    bot.send_photo(
                        id,
                        open(f"{cur_path}/{user_id}/{file_name}", "rb"),
                        reply_markup=markup,
                    )
                else:
                    bot.send_document(
                        id,
                        open(f"{cur_path}/{user_id}/{file_name}", "rb"),
                        reply_markup=markup,
                    )

    return "good"


def start_bot():
    while True:
        try:
            bot.infinity_polling()
        except:
            time.sleep(30)


def start_server():
    app.run(port=8000, host="0.0.0.0")


if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()

    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            break
