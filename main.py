from fastapi import FastAPI, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Body, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import *
from database import *

# создаем приложение
app = FastAPI()

#  путь для передачи статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")


# настриваем каталог шаблонов
templates = Jinja2Templates(directory="templates")

# создаем статический каталог
app.mount('/static', StaticFiles(directory='templates', html=True), name='core')


# создаем таблицы
Base.metadata.create_all(bind=engine)
 
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

# получаем страницу для авторизации специалистов
@app.get('/login_spec')
async def get_login_html(request: Request):
    '''
    We receive a page for log in

    Docstring for get_login_html
    
    :param request: Description
    :type request: Request
    '''

    return templates.TemplateResponse("login_spec.html", {'request' : request})


# получаем страницу для авторизации пациентов
@app.get('/login_patient')
async def get_login_html(request: Request):
    '''
    We receive a page for log in

    Docstring for get_login_html
    
    :param request: Description
    :type request: Request
    '''

    return templates.TemplateResponse("login_patient.html", {'request' : request})

# получаем страницу для регистрации специалистов

@app.get('/registration_spec')
async def get_registration_html(request: Request):
    '''
    We receive a page for registration

    Docstring for get_registration_html
    
    :param request: Description
    :type request: Request
    '''

    return templates.TemplateResponse("registration_spec.html", {'request' : request})

# получаем страницу для регистрации пациентов

@app.get('/registration_patient')
async def get_registration_html(request: Request):
    '''
    We receive a page for registration

    Docstring for get_registration_html
    
    :param request: Description
    :type request: Request
    '''

    return templates.TemplateResponse("registration_patient.html", {'request' : request})


# отправляем данные зарегистрированного пользователя на БД
@app.post('/registration_spec')
async def registration_spec(data = Body(), db: Session = Depends(get_db)):

    '''
    We send the created userdata to the database

    Docstring for registration_spec
    
    :param data: Description
    :param db: Description
    :type db: Session
    :return: Description
    :rtype: Specialists
    '''
 


    specialists = Specialists(
                    gender = data['gender'],   
                      first_name = data['first_name'],  
                        last_name = data['last_name'],
                            speccode = data['speccode'], 
                                username = data['username'],
                                    email = data['email'],
                                        phone = data['phone'], 
                                            password = data['password']
                        )
    
    speccode = '1111'
    
    specialists_exists = db.query(Specialists).filter(
        (Specialists.email == specialists.email) | (Specialists.username == specialists.username) | (Specialists.speccode == specialists.speccode)
    ).first()
    if specialists_exists: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином, почтой или кодом доступа уже зарегистрирован"
        )

    elif specialists.speccode != speccode:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Код специалиста не найден"
        )

    else: 

        db.add(specialists)   
        db.commit()
        db.refresh(specialists)
        


    return {"status": "ok"}



# проверяем полученные данные пользователя при авторизации 
@app.post('/login_spec')
async def login_spec(data: dict = Body(), db: Session = Depends(get_db)):

    '''
    We check the userdata to the database

    Docstring for login_spec
    
    :param data: Description
    :param db: Description
    :type db: Session
    :return: Description
    :rtype: Specialists
    '''
 
    username = data.get('username')
    password = data.get('password')

    specialists_exists = db.query(Specialists).filter(
        (Specialists.username == username) & (Specialists.password == password)).first()
    if not specialists_exists: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )

    return {"message": "Успешный вход", "user": username}


# отправляем данные зарегистрированного пользователя на БД
@app.post('/registration_patient')
async def registration_patient(data = Body(), db: Session = Depends(get_db)):
 
    '''
    We send the created userdata to the database

    Docstring for registration_patient
    
    :param data: Description
    :param db: Description
    :type db: Session
    :return: Description
    :rtype: Patients
    '''


    patients = Patients(
                    gender = data['gender'],   
                      first_name = data['first_name'],  
                        last_name = data['last_name'],
                            username = data['username'],
                                email = data['email'],
                                    phone = data['phone'], 
                                        password = data['password']
                        )
    
    patients_exists = db.query(Patients).filter(
        (Patients.email == patients.email) | (Patients.username == patients.username) 
    ).first()
    if patients_exists: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином или почтой доступа уже зарегистрирован"
        )

    else: 

        db.add(patients)   
        db.commit()
        db.refresh(patients)
        


    return {"status": "ok"}


# проверяем полученные данные пользователя при авторизации 
@app.post('/login_patient')
async def login_patient(data: dict = Body(), db: Session = Depends(get_db)):

    '''
    We check the userdata to the database

    Docstring for login_patient
    
    :param data: Description
    :param db: Description
    :type db: Session
    :return: Description
    :rtype: Patients
    '''
 
    username = data.get('username')
    password = data.get('password')
    
    patient_exists = db.query(Patients).filter(
        (Patients.username == username) & (Patients.password == password)).first()
    if not patient_exists: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )

    return {"message": "Успешный вход", "user": username} 