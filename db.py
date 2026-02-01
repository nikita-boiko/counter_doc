from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

# адрес базы данных для подключения
DATABASE_URL =  os.getenv('DATABASE_URL')

# создаем движок для взаимодействия с БД
engine = create_engine(DATABASE_URL)

# создаем сессию работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# создаем модель базы данных
class Base(DeclarativeBase): pass
class Doctors(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    speciality = Column(String)
    name = Column(String)
    date_record = Column(DateTime)
    record = Column(Boolean)
    patient = Column(String)



    

