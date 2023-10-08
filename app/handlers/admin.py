from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import app.database.requests as db
import app.keyboards.admin as kb
import os
from dotenv import load_dotenv
from app.app_data.data import Data
from bot import bot

data = Data()
load_dotenv()
storage = MemoryStorage()
admin_router = Router()
router = admin_router

class Code(StatesGroup):
    code = State()

class Video_a(StatesGroup):
    change = State()
    finish = State()

class Mailing(StatesGroup):
    get_photo = State()
    finish = State()
    confirmation = State()

# Admin Initialization
@router.message(F.text == '/admin')
async def check(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Добро пожаловать, админ', reply_markup=kb.main_admin_kb)
    else:
        await message.answer('Я вас не понимаю')


# Replacing the code word
@router.message(F.text == 'Заменить кодовое слово')
async def change_code(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Введите новое кодовое слово:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Code.code)
    else:
        await message.answer('Я вас не понимаю')

@router.message(Code.code)
async def change(message: Message, state: FSMContext):
    new_code = message.text
    data.code_word('change', text=new_code)
    await message.answer(f'Кодовое слово успешно заменено на: {new_code}', reply_markup=kb.main_admin_kb)
    await state.clear()






# Video Replacement
@router.message(F.text == 'Заменить видео')
async def change_video(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Какое из видео вы хотите заменить?', reply_markup=kb.change_video_kb)
        await state.set_state(Video_a.change)
    else:
        await message.answer('Я вас не понимаю')

@router.message(Video_a.change)
async def change_video(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Пришлите видео на замену', reply_markup=kb.cancel_kb)
    await state.set_state(Video_a.finish)

@router.message(lambda message: not message.video and message.text != 'Отмена', Video_a.finish)
async def add_item_photo(message: Message, state: FSMContext):
    await message.answer('Пришлите видео или нажмите "Отмена"')

@router.message(Video_a.finish)
async def finish(message: Message, state: FSMContext):
    try:

        if message.text == 'Отмена':
            await message.answer('Отмена замены', reply_markup=kb.main_admin_kb)
            await state.clear()

        else:
            data_1 = await state.get_data()
            name = data_1['name']
            video = message.video.file_id
            data.video('change', name=name, video=video)
            await message.answer(f'Видео №{name} было успешно заменено!', reply_markup=kb.main_admin_kb)
            await state.clear()
    except:
        await message.answer('К сожалению, видео слишком тяжелое, и Телеграм его не пропускает. Попробуйте еще раз.')
        await state.set_state(Video_a.finish)


# Creating a mailing list
@router.message(F.text == 'Сделать рассылку')
async def mailing(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Пришлите фото для рассылки. Если фото не нужно, просто нажмите "Пропустить".', reply_markup=kb.yes_or_no_kb)
        await state.set_state(Mailing.get_photo)
    else:
        await message.answer('Я вас не понимаю')

@router.message(lambda message: not message.photo and message.text != 'Пропустить' and message.text != 'Отмена', Mailing.get_photo)
async def add_item_photo(message: Message, state: FSMContext):
    await message.answer('Пришлите фото или нажмите "Пропустить"')

@router.message(Mailing.get_photo)
async def add(message: Message, state: FSMContext):

    if message.text == 'Пропустить':
        await state.update_data(photo='None')
        await message.answer('Пришлите текст рассылки', reply_markup=kb.cancel_kb)
        await state.set_state(Mailing.finish)

    elif message.text == 'Отмена':
        await message.answer('Отмена рассылки', reply_markup=kb.main_admin_kb)
        await state.clear()

    else:
        await state.update_data(photo=message.photo[-1].file_id)
        await message.answer('Пришлите текст рассылки', reply_markup=kb.cancel_kb)
        await state.set_state(Mailing.finish)


# Exception Handling telegram
@router.message(Mailing.finish)
async def start_mailing(message: Message, state: FSMContext):
    try:
        if message.text == 'Отмена':
            await message.answer('Отмена рассылки', reply_markup=kb.main_admin_kb)
            await state.clear()

        else:
            await state.update_data(text=message.text)
            data_m = await state.get_data()
            photo = data_m['photo']
            text = data_m['text']
            if photo == 'None':
                await message.answer(text=f'<b>Ваша рассылка:</b> \n\n'
                                    f'{text}', parse_mode='html', reply_markup=kb.confirmation_kb)
                
            else:
                await message.answer_photo(photo=photo,
                                        caption=f'<b>Ваша рассылка:</b> \n\n'
                                        f'{text}', parse_mode='html', reply_markup=kb.confirmation_kb)
            await state.set_state(Mailing.confirmation)
    except:
        await message.answer('Текст сообщения слишком длинный, и сервера Телеграма не готовы его пропускать. Попробуйте сократить текст и прислать его снова.')
        await state.set_state(Mailing.finish)


# Confirmation of the mailing list
@router.message(Mailing.confirmation)
async def conf(message: Message, state: FSMContext):
    if message.text == 'Отправить':
        data_m = await state.get_data()
        photo = data_m['photo']
        text = data_m['text']
        users = await db.get_ids()
        if photo == 'None':
            for id in users:
                await bot.send_message(chat_id=id,
                                       text=text)
        else:
            for id in users:
                await bot.send_photo(chat_id=id,
                                     photo=photo,
                                     caption=text)
        await message.answer('Сообщение доставлено!', reply_markup=kb.main_admin_kb)
        await state.clear()

    elif message.text == 'Отмена':
        await message.answer('Отмена рассылки', reply_markup=kb.main_admin_kb)
        await state.clear()

    else: 
        await message.answer('Виберите пункт на клавиатуре:')
        await state.set_state(Mailing.confirmation)