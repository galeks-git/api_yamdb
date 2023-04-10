# Проект YaMDb

## Описание
Администратор наполняет проект описаниями произведений в категориях: «Книги», «Фильмы», «Музыка». 
В каждой категории произведения могут классифицироваться по жанрам (Genre).
Зарегистрированные посетители оставляют комментарии (Comment) и ставят оценки произведениям.
Из пользовательских оценок формируется усреднённый рейтинг произведений.

## Как запустить проект:
* Клонировать репозиторий:
```
git clone https://github.com/galeks-git/api_yamdb.git
```

* Cоздать виртуальное окружение:
```
python -m venv venv (Win)
python3 -m venv venv (Linux)
```

* Активировать виртуальное окружение:
```
source venv/scripts/activate (Win)
source venv/bin/activate (Linux)
```

* Установить зависимости из файла requirements.txt:
```
pip install --upgrade pip
pip install -r requirements.txt
```

* Выполнить миграции:
```
python manage.py migrate (Win)
python3 manage.py migrate (Linux)
```

* Заполнить Базу данных из CSV
```
python manage.py load_csv (Win)
python3 manage.py load_csv (Linux)
```

* Запустить проект:
```
python manage.py runserver (Win)
python3 manage.py runserver (Linux)
```

## Примеры некоторых запросов
Все эндпоинты и их методы доступны на: http://127.0.0.1:8000/redoc/

## Авторы
- Александр Горюнов (тимлид, Revews, Comments)
- Богдан Бабийчук (Titles, Categories, Genres)
- Сергей Тарасенко (Authentication, Permissions, Users)