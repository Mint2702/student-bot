from telebot import TeleBot, types
import uuid
import time
import codecs

from core.settings import settings
from core.message_handlers.markups import (
    generate_start_markup,
    generate_work_type_markup,
    generate_tutor_makup,
)
from core import redis_
from core.message_handlers.utils import (
    cancel_order,
    basic_message_decorator,
    calendar_1_callback,
    calendar,
    calendar_markup,
)
from core.message_handlers.order_work_logic import enter_type, day_entered_work
from core.message_handlers.order_help_logic import day_entered_help
from core.message_handlers.find_tutor_logic import enter_study_type


TOKEN = settings.token
bot = TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=["start"])
@basic_message_decorator(bot)
def start(message):
    markup = generate_start_markup()

    bot.send_message(
        message.chat.id,
        f"Приветствуем, {message.from_user.first_name}! Этот бот поможет тебе заказать работу.",
        reply_markup=markup,
    )


@bot.message_handler(regexp="Заказать работу")
@basic_message_decorator(bot)
def order_work(message):
    markup = generate_work_type_markup()

    order_id = str(uuid.uuid4().hex)
    redis_.dump_data(
        message.from_user.id,
        {
            "id": order_id,
            "user_id": message.from_user.id,
            "type": "work",
        },
    )

    bot.send_message(
        message.chat.id,
        f"{message.from_user.first_name}, выберите тип работы:",
        reply_markup=markup,
    )
    time.sleep(0.2)
    msg = bot.send_message(
        message.chat.id,
        f"(Список можно пролистать ниже)",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_type, bot)


@bot.message_handler(regexp="Помощь онлайн")
@basic_message_decorator(bot)
def order_help(message):
    order_id = str(uuid.uuid4().hex)
    redis_.dump_data(
        message.from_user.id,
        {
            "id": order_id,
            "user_id": message.from_user.id,
            "type": "help",
        },
    )

    calendar_markup(message, bot, "Укажите дату")


@bot.message_handler(regexp="репетитор")
@basic_message_decorator(bot)
def find_tutor(message):
    order_id = str(uuid.uuid4().hex)
    redis_.dump_data(
        message.from_user.id,
        {
            "id": order_id,
            "user_id": message.from_user.id,
            "type": "tutor",
        },
    )

    markup = generate_tutor_makup()
    msg = bot.send_message(
        message.chat.id,
        f"Укажите место обучения",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, enter_study_type, bot)


@bot.message_handler(regexp="админ")
def ask_question(message):
    url = f"https://t.me/{settings.manager}"

    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text="Написать админу", url=url)
    markup.add(btn_my_site)
    bot.send_message(
        message.chat.id,
        f"{message.from_user.first_name}, задайте админу свой вопрос.",
        reply_markup=markup,
    )


@bot.message_handler(regexp="Условия")
@basic_message_decorator(bot)
def conditions(message):
    file = codecs.open("core/message_handlers/conditions.txt", "r", "utf_8_sig")
    text = file.read()
    bot.send_message(
        message.chat.id,
        text,
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1_callback.prefix)
)
def callback_inline(call: types.CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )

    type = redis_.load_data(call.from_user.id)["type"]

    if action == "DAY":
        if type == "work":
            day_entered_work(call, date, bot)
        else:
            day_entered_help(call, date, bot)
    elif action == "CANCEL":
        cancel_order(call, bot)


@bot.message_handler(func=lambda m: True)
@basic_message_decorator(bot)
def echo_all(message):
    markup = generate_start_markup()
    bot.reply_to(message, "Простите, неизвестная команда")
    bot.send_message(
        message.chat.id, "Выберите необходимое действие:", reply_markup=markup
    )


while True:
    try:
        bot.infinity_polling()
    except:
        time.sleep(30)
