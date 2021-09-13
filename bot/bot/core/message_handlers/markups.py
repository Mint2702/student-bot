from telebot import types


def generate_start_markup():
    buttons = [
        "🌴 Заказать",
        "📲 Помощь онлайн",
        "🎓 Связь с админом",
        "📰 Условия",
        "👨‍🎓 Найти репетитора 👩‍🎓",
    ]

    markup = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton(buttons[0])
    button2 = types.KeyboardButton(buttons[1])
    button3 = types.KeyboardButton(buttons[2])
    button4 = types.KeyboardButton(buttons[3])
    button5 = types.KeyboardButton(buttons[4])
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)

    return markup


def generate_work_type_markup():
    buttons = [
        "Кандидатская",
        "Дипломная",
        "Докторская",
        "МВА",
        "Отчет по практике",
        "НИР",
        "Реферат",
        "Курсовая",
        "Презентация",
        "Эссе",
        "Научная публикация",
        "ДЗ",
        "Билеты",
        "Другое (Ввести вручную)",
        "Назад",
    ]
    markup = types.ReplyKeyboardMarkup()
    for button_name_index in range(len(buttons) // 2 + 1):
        button_name_index *= 2

        if len(buttons) - button_name_index > 1:
            button1 = types.KeyboardButton(buttons[button_name_index])
            button2 = types.KeyboardButton(buttons[button_name_index + 1])
            markup.row(button1, button2)
        else:
            button = types.KeyboardButton(buttons[button_name_index])
            markup.row(button)

    return markup


def generate_basic_markup(top_button_text: str = "Не знаю"):
    buttons = [top_button_text, "Отмена"]

    markup = types.ReplyKeyboardMarkup()
    for button_name in buttons:
        button = types.KeyboardButton(button_name)
        markup.row(button)

    return markup


def generate_tutor_makup():
    buttons = ["🏢 Университет", "🏫 Школа", "🏣 Колледж", "Отмена"]

    markup = types.ReplyKeyboardMarkup()
    for button_name in buttons:
        button = types.KeyboardButton(button_name)
        markup.row(button)

    return markup


def generate_tutor_sex_makup():
    buttons = ["Мужской", "Женский", "Не важно"]

    markup = types.ReplyKeyboardMarkup()
    for button_name in buttons:
        button = types.KeyboardButton(button_name)
        markup.row(button)

    return markup


def generate_none_user():
    markup = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton("Написать админу")
    markup.row(button)

    return markup
