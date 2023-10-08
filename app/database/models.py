from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///bot.db')

Base = declarative_base()

# Creating a database and a sheet with user data
class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    user_tg_id = Column(Integer, nullable=False)
    user_name = Column(String)
    user_last_name = Column(String)
    user_is_premium = Column(String)
    user_languge = Column(String)
    username = Column(String)
    user_state = Column(String)




start_db = Base.metadata.create_all(engine)