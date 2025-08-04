# TechShop - Интернет-магазин электроники

![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Redis](https://img.shields.io/badge/Redis-6.2+-red.svg)

## 🛍️ Описание проекта

TechShop - это полнофункциональный интернет-магазин электроники, построенный на Django. Проект включает в себя все основные функции современного e-commerce решения: каталог товаров, систему пользователей, корзину покупок, избранное, отзывы, заказы, платежи и рассылку новостей.

## ✨ Реализованный функционал

### 🛍️ Основные возможности
- **Каталог товаров** с категориями и брендами
- **Поиск и фильтрация** товаров по различным критериям
- **Система пользователей** с регистрацией, авторизацией и восстановлением пароля
- **Корзина покупок** с добавлением/удалением товаров
- **Избранное** для сохранения понравившихся товаров
- **Система отзывов** с рейтингами
- **Оформление заказов** с различными способами оплаты
- **Интеграция с PayPal** для онлайн-платежей
- **Рассылка новостей** с уведомлениями о новых товарах
- **Административная панель** для управления контентом

### 🎨 Пользовательский интерфейс
- Адаптивный дизайн с использованием Bootstrap
- Современный UI с анимациями и интерактивными элементами
- AJAX-фильтрация товаров без перезагрузки страницы
- Система уведомлений и сообщений
- Пагинация для больших списков товаров

### 🔧 Технические особенности
- Кеширование с использованием Redis
- Асинхронные задачи с Celery
- Система тестирования с pytest
- Оптимизированные запросы к базе данных
- Безопасная обработка платежей
- Валидация форм и данных

## 🛠️ Технологический стек

### Backend
- **Django 5.2.4** - основной веб-фреймворк
- **Python 3.13** - язык программирования
- **PostgreSQL** - основная база данных
- **Redis** - кеширование и брокер сообщений
- **Celery** - асинхронные задачи
- **PayPal REST SDK** - интеграция платежей

### Frontend
- **Bootstrap** - CSS-фреймворк
- **jQuery** - JavaScript библиотека
- **Slick Carousel** - слайдеры
- **Font Awesome** - иконки
- **AJAX** - асинхронные запросы

### Инструменты разработки
- **pytest** - тестирование
- **Black** - форматирование кода
- **django-environ** - управление переменными окружения
- **Pillow** - обработка изображений

## 📁 Структура проекта

```
techshop/
├── accounts/          # Система пользователей
├── carts/            # Корзина покупок
├── favorites/        # Избранное
├── newsletters/      # Рассылка новостей
├── orders/           # Заказы
├── payments/         # Платежи
├── reviews/          # Отзывы
├── store/            # Основной каталог товаров
├── techshop/         # Настройки проекта
├── media/            # Загруженные файлы
└── requirements.txt  # Зависимости
```

## 🚀 Установка и запуск

### Предварительные требования
- Python 3.13+
- PostgreSQL 15+
- Redis 6.2+
- Git

### Пошаговая инструкция

1. **Клонирование репозитория**
   ```bash
   git clone <repository-url>
   cd techshop
   ```

2. **Создание виртуального окружения**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. **Установка зависимостей**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройка базы данных PostgreSQL**
   ```sql
   CREATE DATABASE techshop_db;
   CREATE USER techshop_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE techshop_db TO techshop_user;
   ```

5. **Создание файла .env**
   ```bash
   cp .env.example .env
   ```
   
   Заполните файл `.env` следующими данными:
   ```env
   # Django settings
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DOMAIN=http://localhost:8000

   # Database settings
   DB_NAME=techshop_db
   DB_USER=techshop_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432

   # Email settings
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com

   # Celery settings
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0

   # PayPal settings
   PAYPAL_CLIENT_ID=your-paypal-client-id
   PAYPAL_CLIENT_SECRET=your-paypal-client-secret
   PAYPAL_MODE=sandbox
   PAYPAL_CURRENCY=USD

   # Cache settings
   CACHE_LOCATION=redis://localhost:6379/1
   ```

6. **Запуск Redis**
   ```bash
   redis-server
   ```

7. **Применение миграций**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Создание суперпользователя**
   ```bash
   python manage.py createsuperuser
   ```

9. **Загрузка тестовых данных (опционально)**
   ```bash
   python manage.py loaddata category_data.json
   python manage.py loaddata brand_data.json
   python manage.py loaddata product_data.json
   ```

10. **Запуск Celery (в отдельном терминале)**
    ```bash
    celery -A techshop worker -l info
    ```

11. **Запуск сервера разработки**
    ```bash
    python manage.py runserver
    ```

12. **Открытие в браузере**
    ```
    http://localhost:8000
    ```

## 🧪 Тестирование

Проект включает комплексную систему тестирования:

```bash
# Запуск всех тестов
pytest

# Запуск тестов с покрытием
pytest --cov

# Запуск тестов конкретного приложения
pytest accounts/
pytest store/
pytest carts/
```

## 📊 Основные модели данных

- **User** - пользователи системы
- **Category** - категории товаров
- **Brand** - бренды
- **Product** - товары
- **CartItem** - позиции корзины
- **Favorite** - избранные товары
- **Review** - отзывы
- **Order** - заказы
- **OrderItem** - позиции заказов
- **Payment** - платежи
- **Subscriber** - подписчики рассылки

## 🔒 Безопасность

- CSRF защита
- Валидация форм
- Безопасная обработка платежей
- Хеширование паролей
- Защита от SQL-инъекций
- Валидация входных данных

## ⚡ Производительность

- Кеширование с Redis
- Оптимизированные запросы к БД
- Пагинация больших списков
- Сжатие статических файлов
- Асинхронная обработка задач