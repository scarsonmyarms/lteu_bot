from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_kb():
    kb_list = [
        [KeyboardButton(text="Вступникам"), KeyboardButton(text="Магістратура")],
        [KeyboardButton(text="Іноземним студентам"), KeyboardButton(text="Аспірантура")],
        [KeyboardButton(text="Контакти")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def vstupnik_kb():
    kb_list = [
        [KeyboardButton(text="Вартість навчання"), KeyboardButton(text="Інформація про гуртожиток")],
        [KeyboardButton(text="Необхідні документи для зарахування"), KeyboardButton(text="Список спеціальностей")],
        [KeyboardButton(text='Назад')]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


