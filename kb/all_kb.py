from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType, InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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

def magistr_kb():
    kb_list = [
        [KeyboardButton(text="спеціальності"), KeyboardButton(text="ціна")],
        [KeyboardButton(text='Назад')]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

