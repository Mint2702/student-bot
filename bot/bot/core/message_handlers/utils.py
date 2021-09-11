from loguru import logger
import datetime

from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData

from ..db.requests import get_user, post_user
from .markups import generate_start_markup, generate_none_user


calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")


def basic_message_decorator(bot):
    def decorator(func):
        def wrapper(message, *args, **kwargs):
            if not _post_new_user(message):
                logger.error("Some error occured while registering")
                none_user(message, bot)
                return

            if message.text == "Отмена" or message.text == "Назад":
                cancel_order(message, bot)
            else:
                try:
                    func(message, *args, **kwargs)
                except Exception as err:
                    logger.error("Some error occured while handling message.")
                    logger.warning(err)

        return wrapper

    return decorator


def basic_message_decorator_no_arg(func):
    def wrapper(message, bot, *args, **kwargs):
        _post_new_user(message)
        if message.text == "Отмена" or message.text == "Назад":
            cancel_order(message, bot)
        else:
            try:
                func(message, bot, *args, **kwargs)
            except Exception as err:
                logger.error("Some error occured while handling message.")
                logger.warning(err)

    return wrapper


@basic_message_decorator_no_arg
def calendar_markup(message, bot, string):
    now = datetime.datetime.now()  # Get the current date
    bot.send_message(
        message.chat.id,
        f"Постараемся вам помочь. \n{string}:",
        reply_markup=calendar.create_calendar(
            name=calendar_1_callback.prefix,
            year=now.year,
            month=now.month,  # Specify the NAME of your calendar
        ),
    )


def cancel_order(message, bot):
    markup = generate_start_markup()
    bot.send_message(
        chat_id=message.from_user.id,
        text="Оформление заказа отменено",
        reply_markup=markup,
    )


def none_user(message, bot):
    markup = generate_none_user()
    bot.send_message(
        chat_id=message.from_user.id,
        text="У Вас скрыт ник, Вы не можете заказать работу в боте - напишите нашему менеджеру, он с Вами договорится лично",
        reply_markup=markup,
    )


def _post_new_user(message):
    user = get_user(message.from_user.id)
    if user == []:
        user = {
            "id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
        }
        if post_user(user):
            return True
        else:
            return False
    return True
