# Doctor Appointment Management System

## Project Description

This is a web application developed using the **FastAPI** framework for managing patient appointments with various specialists. The system allows administrators and specialists to manage available time slots, while patients can view analytics and book appointments. Interaction with the database (DB) is implemented via **SQLAlchemy ORM**, and **Jinja2** templates are used for displaying the pages.

## Technologies Used

*   **Python**
*   **FastAPI**: A modern, fast web framework for building APIs.
*   **SQLAlchemy**: A library for working with databases (ORM).
*   **Jinja2Templates**: A template engine for server-side HTML generation.
*   **Static files (HTML, CSS, JS)**: Used for frontend and styling.
*   **Database**: Uses a `db` abstraction (presumably SQLite, PostgreSQL, or MySQL).

## Core Functionality

*   **Main Page (`/`)**: Displays the administrator page (`admin.html`).
*   **Specialist Page (`/specialist`)**: Provides access to the interface for specialists (`specialist.html`).
*   **Slot Management (`/specialist/slots`)**: A page for creating new appointment slots and submitting them to the DB.
*   **Analytics (`/analytics`, `/analytics/{speciality}`)**: View statistics by specialty and filter doctors by the selected specialty.
*   **Patient Booking (`/record`, `/record/{speciality}`)**: An interface for patients to book appointments, which updates the slot status in the DB.
*   **API Endpoints**:
    *   `POST /slots`: Creates a new appointment slot in the DB.
    *   `PUT /record`: Updates the appointment slot status and adds the patient's full name.

## Installation and Launch

To run the project, you will need **Python >= 3.7** (or newer).

1.  Clone the repository.
2.  Install the necessary dependencies, most likely using `pip` (a specific list can be found in the `requirements.txt` or `pyproject.toml` file, if they exist). Example:

    ```bash
    pip install "fastapi[standard]" uvicorn sqlalchemy jinja2
    ```

3.  Ensure that the template files (HTML) and static files are located in the respective directories (`templates/` and `static/`, which are mounted in the application).
4.  Launch the application using `uvicorn`:

    ```bash
    uvicorn main:app --reload
    ```

5.  Open in your browser: `http://127.0.0.1:8000`

The project uses FastAPI's dependency injection system to manage database sessions.


# Система управления записями к врачам

## Описание проекта

Это веб-приложение, разработанное с использованием фреймворка **FastAPI**, для управления записями пациентов к различным специалистам. Система позволяет администраторам и специалистам управлять доступными временными слотами, а пациентам — просматривать аналитику и записываться на прием. Взаимодействие с базой данных (БД) реализовано через **SQLAlchemy ORM**, а для отображения страниц используются **Jinja2** шаблоны.

## Используемые технологии

*   **Python**
*   **FastAPI**: Современный, быстрый веб-фреймворк для API.
*   **SQLAlchemy**: Библиотека для работы с базами данных (ORM).
*   **Jinja2Templates**: Движок шаблонов для генерации HTML-страниц на стороне сервера.
*   **Статические файлы (HTML, CSS, JS)**: Для фронтенда и стилизации.
*   **База данных**: Используется абстракция `db` (предположительно SQLite, PostgreSQL или MySQL).

## Основной функционал

*   **Главная страница (`/`)**: Отображает страницу администратора (`admin.html`).
*   **Страница специалистов (`/specialist`)**: Доступ к интерфейсу для специалистов (`specialist.html`).
*   **Управление слотами (`/specialist/slots`)**: Страница для создания новых талонов и отправки их в БД.
*   **Аналитика (`/analytics`, `/analytics/{speciality}`)**: Просмотр статистики по специальностям и фильтрация врачей по выбранной специальности.
*   **Запись пациентов (`/record`, `/record/{speciality}`)**: Интерфейс для записи пациентов на прием, который обновляет статус талона в БД.
*   **API Эндпоинты**:
    *   `POST /slots`: Создание нового талона в БД.
    *   `PUT /record`: Обновление статуса талона и добавление ФИО пациента.

## Установка и запуск

Для запуска проекта вам потребуется **Python >= 3.7** (или выше).

1.  Клонируйте репозиторий.
2.  Установите необходимые зависимости, скорее всего, используя `pip` (конкретный список можно найти в файле `requirements.txt` или `pyproject.toml`, если они есть). Пример:

    ```bash
    pip install "fastapi[standard]" uvicorn sqlalchemy jinja2
    ```

3.  Убедитесь, что файлы шаблонов (HTML) и статические файлы находятся в соответствующих директориях (`templates/` и `static/`, которые монтируются в приложении).
4.  Запустите приложение с помощью `uvicorn`:

    ```bash
    uvicorn main:app --reload
    ```

5.  Откройте в браузере: `http://127.0.0.1:8000`

Проект использует систему внедрения зависимостей FastAPI для управления сессиями БД.


