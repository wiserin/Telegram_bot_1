from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import app.database.requests as db
import app.keyboards.user as kb
from app.app_data.data import Data
import os
from bot import bot

data = Data()

storage = MemoryStorage()
user_router = Router()
router = user_router

class Check_code(StatesGroup):
    check = State()

class Video(StatesGroup):
    first = State()
    first_H = State()
    second = State()
    second_H = State()
    third = State()
    third_H = State()
    finish = State()

# User Initialization
@router.message(F.text == '/start')
async def start(message: Message, state: FSMContext):
    user = await db.initialization(message.from_user.id)

    if user == True:
        await message.answer('Добро пожаловать!', reply_markup=kb.start_kb)
        await state.set_state(Video.first)

    elif user == False:
        await message.answer('Для получения доступа к урокам, введите кодовое слово')
        await state.set_state(Check_code.check)

# Code word verification
@router.message(Check_code.check)
async def check_code(message: Message, state: FSMContext):
    code = data.code_word('check', code_word=message.text)

    if code == True:
        await message.answer('Вы зарегистрированы', reply_markup=kb.start_kb)
        await db.add_new_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.is_premium, 
                              message.from_user.language_code, message.from_user.username)
        await state.clear()
        await state.set_state(Video.first)

    elif code == False:
        await message.answer('Не правельный код. Попробуйте снова')
        await state.set_state(Check_code.check)




# Sending a video
@router.message(Video.first)
async def first_video(message: Message, state: FSMContext):
    video = data.video('read', name='1')
    await message.answer_video(video=video, 
                               caption='Первое видео', reply_markup=kb.first_HW_kb)
    await state.set_state(Video.first_H)

@router.message(Video.first_H)
async def first_HW(message: Message, state: FSMContext):
    await message.answer('Пришлите ДЗ на проверку', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Video.second)

@router.message(Video.second)
async def second_video(message: Message, state: FSMContext):
    video = data.video('read', name='2')
    await message.answer_video(video=video,
                               caption='Второе видео', reply_markup=kb.second_HW_kb)
    await state.set_state(Video.second_H)

@router.message(Video.second_H)
async def second_HW(message: Message, state: FSMContext):
    await message.answer('Пришлите ДЗ на проверку', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Video.third)

@router.message(Video.third)
async def third_video(message: Message, state: FSMContext):
    video = data.video('read', name='3')
    await message.answer_video(video=video,
                               caption='Третье видео', reply_markup=kb.third_HW_kb)
    await state.set_state(Video.third_H)

@router.message(Video.third_H)
async def third_HW(message: Message, state: FSMContext):
    await message.answer('Пришлите ДЗ на проверку', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Video.finish)

@router.message(Video.finish)
async def finish_u(message: Message, state: FSMContext):
    await message.answer('Поздравляем! Вы посмотрели все видео!')
    await state.clear()



# Response to an incomprehensible message
@router.message()
async def nothing(message: Message):
    await message.answer('Я вас не понимаю')