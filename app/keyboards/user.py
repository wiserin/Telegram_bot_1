from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)
import app.database.requests as db

start = [
    [KeyboardButton(text='Начать')]
]
start_kb = ReplyKeyboardMarkup(keyboard=start,
                               resize_keyboard=True)

first_HW = [
    [KeyboardButton(text='Прислать первое ДЗ')]
]
first_HW_kb = ReplyKeyboardMarkup(keyboard=first_HW,
                                  resize_keyboard=True)

second_HW = [
    [KeyboardButton(text='Прислать второе ДЗ')]
]
second_HW_kb = ReplyKeyboardMarkup(keyboard=second_HW,
                                  resize_keyboard=True)

third_HW = [
    [KeyboardButton(text='Прислать третье ДЗ')]
]
third_HW_kb = ReplyKeyboardMarkup(keyboard=third_HW,
                                  resize_keyboard=True)