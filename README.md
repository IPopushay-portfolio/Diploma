## Проект -"Learning Modules Platform"
Платформа для управления образовательными модулями.

## Описание
Backend-сервис для управления образовательными модулями с функционалом:
- Управление курсами и модулями
- Система ролей (студент, преподаватель)
- Загрузка учебных материалов
- Отслеживание прогресса обучения

## Структура проекта
learning_modules/
├── config/                 # Настройки Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                  # Приложение пользователей
│   ├── models.py          # Модель CustomUser
│   ├── serializers.py
│   ├── views.py
│   └── tests/
├── lm/                    # Основное приложение
│   ├── models.py          # Модели Course, Module, Material, Enrollment
│   ├── serializers.py
│   ├── views.py
│   └── tests/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── pyproject.toml         # Зависимости Poetry
├── README.md
└── .gitignore

# Модели
- CustomUser
Роли: student, teacher
Связи с курсами и модулями

- Course (Курс)
Основная информация о курсе
Связь с преподавателем

- EducationalModule (Модуль)
Порядковый номер в курсе
Связи с материалами

- Material (Материал)
Различные типы контента
Загрузка файлов

- Enrollment (Запись)
Прогресс обучения
Статус прохождения

# Права доступа
- Преподаватели могут:
Создавать и редактировать курсы
Управлять модулями
Загружать материалы

- Студенты могут:
Просматривать курсы и модули
Записываться на модули
Отслеживать свой прогресс

## Установка и настройка проекта:
1. Создание проекта и виртуального окружения
   # Активация виртуального окружения Poetry
     - poetry shell
   
2. Установка зависимостей
   # Установка Django
     - poetry add django
   # Установка PostgreSQL
     - poetry add psycopg2-binary   
   # Установка библиотеки для работы с переменными окружения
     - poetry add python-dotenv
   # Установка Celery для асинхронных задач
     - poetry add celery

# Разработка
- Создание новых миграций
poetry run python manage.py makemigrations

- Применение миграций
poetry run python manage.py migrate

- Запуск сервера разработки
poetry run python manage.py runserver

# Запуск через Docker
- Сборка и запуск
docker-compose up --build

- Создание миграций
docker-compose run web python manage.py makemigrations

- Применение миграций
docker-compose run web python manage.py migrate

- Создание суперпользователя
docker-compose run web python manage.py createsuperuser

## Тестирование
- Запуск всех тестов
poetry run pytest

- Запуск с coverage
poetry run pytest --cov=.

- Проверка стиля кода, сортировка импортов, форматирование кода
poetry run flake8, isort, black

## Документация:

Дополнительную информацию о структуре проекта и API можно найти в [документации]

## Лицензия:

Проект распространяется под [лицензией MIT]