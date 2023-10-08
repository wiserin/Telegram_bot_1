from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))