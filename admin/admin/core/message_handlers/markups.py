from telebot import types


def generate_markup():
    markup = types.ReplyKeyboardMarkup()

    button = types.KeyboardButton("Статистика")
    markup.row(button)

    button = types.KeyboardButton("Количество пользователей")
    markup.row(button)

    return markup
