from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)
import app.database.requests as db

# Admin's main keyboard
main_admin = [
    [KeyboardButton(text='Заменить кодовое слово'),
    KeyboardButton(text='Заменить видео')],
    [KeyboardButton(text='Сделать рассылку')]
]
main_admin_kb = ReplyKeyboardMarkup(keyboard=main_admin,
                                    resize_keyboard=True)

# Video selection keyboard for replacement
change_video = [
    [KeyboardButton(text='1')],
    [KeyboardButton(text='2')],
    [KeyboardButton(text='3')]
]
change_video_kb = ReplyKeyboardMarkup(keyboard=change_video,
                                      resize_keyboard=True)

# Keyboard for skipping photos when sending out
yes_or_no = [
    [KeyboardButton(text='Пропустить')],
    [KeyboardButton(text='Отмена')]
]
yes_or_no_kb = ReplyKeyboardMarkup(keyboard=yes_or_no,
                                   resize_keyboard=True)

# The confirmation keyboard for sending the newsletter
confirmation = [
    [KeyboardButton(text='Отправить')],
    [KeyboardButton(text='Отмена')]
]
confirmation_kb = ReplyKeyboardMarkup(keyboard=confirmation,
                                      resize_keyboard=True)

# Cancel button
cancel = [
    [KeyboardButton(text='Отмена')]
]
cancel_kb = ReplyKeyboardMarkup(keyboard=cancel,
                                resize_keyboard=True)