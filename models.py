from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base 

class Doctors(Base):
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True, index=True)
    speciality = Column(String)
    name = Column(String)
    date_record = Column(DateTime)
    record = Column(Boolean)
    patient = Column(String)

class Patients(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    password = Column(String)

class Specialists(Base):
    __tablename__ = "specialists"
    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    speccode = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    password = Column(String)

class Code(Base):
    __tablename__ = "code"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True)
