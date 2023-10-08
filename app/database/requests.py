from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import (Base, User)
import asyncio

engine = create_engine('sqlite:///bot.db')

session = sessionmaker(bind=engine)
s = session()

# Confirmation of user registration
async def initialization(tg_id):
    user = s.query(User).filter(User.user_tg_id == tg_id).one_or_none()
    if user == None:
         return False
    else:
        return True

# Adding information about a new user
async def add_new_user(tg_id, user_name, user_last_name, premium, languge, username):
        new_user = User(user_tg_id=tg_id, user_name=user_name, user_last_name=user_last_name,
                        user_is_premium=premium, user_languge=languge, username=username)
        s.add(new_user)
        s.commit()

# Receiving all user IDs telegrams for mailing
async def get_ids():
     r = []
     for i in s.query(User.user_tg_id):
          r.append(i[0])
     s.commit()
     return r
          