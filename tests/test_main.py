from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# тест основной страницы
def test_read_home_html():

    response = client.get('/')

    # проверяем статус
    assert response.status_code == 200

    # проверяем заголовки
    assert 'text/html' in response.headers['content-type']

    # ищем куски кода в тексте страницы
    assert '<h1>Главное меню</h1>' in response.text

def test_read_specialist_html():

    response = client.get('/specialist')

    # проверяем статус
    assert response.status_code == 200

    # проверяем заголовки
    assert 'text/html' in response.headers['content-type']

    # ищем куски кода в тексте страницы
    assert '<a href="specialist/slots">Добавить талоны</a>' in response.text

def test_read_slots_html():

    response = client.get('/specialist/slots')

    # проверяем статус
    assert response.status_code == 200

    # проверяем заголовки
    assert 'text/html' in response.headers['content-type']

    # ищем куски кода в тексте страницы
    assert '<title>Добавление талонов для записи</title>' in response.text

def test_post_slots_():

    # передаем данные 

    response = client.post('/slots', json={'speciality':'Врач-терапевт', 
                                           'name':'Егоров П.М.',
                                           'date_record': "2026.02.02 13:00:00",
                                            'record': True})

    # проверяем статус
    assert response.status_code == 200

    # проверка совпадения передоваемых данных

    result = response.json()
    assert result['name'] == 'Егоров П.М.'

def test_put_record_():

    # обновляем данные 

    response = client.put('/record', json={ 
                                           'name':'Егоров П.М.',
                                           'date_record': "2026.02.02 13:00:00",
                                           'record': False, 
                                           'patient': 'Иванов И.И.'
                                            })

    # проверяем статус
    assert response.status_code == 200

    # проверка совпадения передоваемых данных

    result = response.json()
    assert result['patient'] == 'Иванов И.И.'
