from fastapi import FastAPI
from db import *
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Body, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_

# создаем приложение
app = FastAPI()


# настриваем каталог шаблонов
templates = Jinja2Templates(directory="templates")

# создаем статический каталог
app.mount('/static', StaticFiles(directory='templates', html=True), name='core')


# создаем таблицы
Base.metadata.create_all(bind=engine)
 
# определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# настриваем отображение основной страницы
@app.get("/", response_class=HTMLResponse, summary='Using the main page')
async def read_data(request: Request):
    '''
    Customizing the display of the main page

    Docstring for read_data
    
    :param request: Description
    :type request: Request
    '''

    return templates.TemplateResponse('index.html', {'request' : request})

# получаем страницу для специалистов
@app.get('/specialist')
async def get_specialist_html(request: Request):
    '''
    We get a page for specialists   

    Docstring for get_specialist_html
    
    :param request: Description
    :type request: Request
    '''


    return templates.TemplateResponse("specialist.html", {'request' : request})

# получаем страницу для создания талонов
@app.get('/specialist/slots')
async def get_doctors_html(request: Request):
    '''
    We get a page for creating coupons

    Docstring for get_doctors_html
    
    :param request: Description
    :type request: Request
    '''


    return templates.TemplateResponse("slots.html", {'request' : request})

# отправляем созданный талон в БД
@app.post('/slots')
def create_slots(data = Body(), db: Session = Depends(get_db)):
    '''
    We send the created coupon to the database

    Docstring for create_slots
    
    :param data: Description
    :param db: Description
    :type db: Session
    :return: Description
    :rtype: Doctors
    '''



    doctors = Doctors(speciality = data['speciality'],
                      name = data['name'],   
                      date_record = data['date_record'],  
                      record = data['record'])    
    db.add(doctors)   
    db.commit()
    db.refresh(doctors)
    return doctors

# получаем страницу аналитики по специальностям 
@app.get('/analytics')
async def get_analytics_html(request: Request):
    '''
    We receive a page of analytics by specialty

    Docstring for get_analytics_html
    
    :param request: Description
    :type request: Request
    '''


    return templates.TemplateResponse("analytics.html", {'request' : request})

# получаем аналитику по выбранной специальности
@app.get("/analytics/{speciality}", response_class=HTMLResponse)
async def get_speciality(request:Request, speciality:str):
    '''
    We receive analytics on the chosen specialty


    Docstring for get_speciality
    
    :param request: Description
    :type request: Request
    :param speciality: Description
    :type speciality: str
    '''


    db = SessionLocal()
    try:
        # фильтруем врачей по специальности
        
        data = db.query(Doctors).filter(
            Doctors.speciality.ilike(f"%{speciality}")
        ).all()
        return templates.TemplateResponse('doctors.html', {'request': request, "data": data, "speciality": speciality})
    finally:
        db.close()


# получаем страницу для записи пациента
@app.get('/record')
async def get_specialist_html(request: Request):
    '''
    We receive a page for patient registration

    Docstring for get_specialist_html
    
    :param request: Description
    :type request: Request
    '''

    return templates.TemplateResponse("record.html", {'request' : request})

# получаем страницу для записи по конкретной специальности
@app.get("/record/{speciality}", response_class=HTMLResponse)
async def get_speciality(request:Request, speciality:str):
    '''
    We receive a page for registration for a specific specialty

    Docstring for get_speciality
    
    :param request: Description
    :type request: Request
    :param speciality: Description
    :type speciality: str
    '''


    db = SessionLocal()
    try:
        # фильтруем врачей по специальности
        data = db.query(Doctors).filter(
            Doctors.speciality.ilike(f"%{speciality}")
        ).all()
        return templates.TemplateResponse('record_doctors.html', {'request': request, "data": data, "speciality": speciality})
    finally:
        db.close()

# Меняем статус талона после записи пациента и вноситься ФИО пациента 
@app.put("/record")
def edit_status(data  = Body(), db: Session = Depends(get_db)):
    '''
    We change the status of the coupon after the patient's 
    registration and enter the patient's full name

    Docstring for edit_status
    
    :param data: Description
    :param db: Description
    :type db: Session
    '''



    db_record = db.query(Doctors).filter(
        and_(
            Doctors.name == data["name"],
            Doctors.date_record == data['date_record'],
        )
    ).first()
    db_record.name = data['name']
    db_record.date_record = data['date_record']
    db_record.record = data["record"]
    db_record.patient = data['patient']
    db.commit() # сохраняем изменения 
    db.refresh(db_record)
    return data

