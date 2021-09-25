from telebot import types


def generate_markup():
    markup = types.ReplyKeyboardMarkup()

    button = types.KeyboardButton("Статистика")
    markup.row(button)

    button = types.KeyboardButton("Количество пользователей")
    markup.row(button)

    button = types.KeyboardButton("Рассылка")
    markup.row(button)

    return markup


def generate_check_message_all_markup():
    markup = types.ReplyKeyboardMarkup()

    button = types.KeyboardButton("Подтвердить")
    markup.row(button)

    button = types.KeyboardButton("Отменить")
    markup.row(button)

    return markup


def generate_decline_markup():
    markup = types.ReplyKeyboardMarkup()

    button = types.KeyboardButton("Отменить")
    markup.row(button)

    return markup
