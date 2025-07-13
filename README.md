# 📦 Electronics Network

**Electronics Network** — система управления иерархической сетью по продаже электроники: заводы, дистрибьюторы, дилеры, розничные сети. Поддерживает REST API, Swagger-документацию, административную панель и командную работу с данными.

---

## 🚀 Технологии и зависимости

- Python 3.13+
- Django 5.2.4
- Django REST Framework 3.16.0
- PostgreSQL (через `psycopg2`)
- DRF YASG (Swagger UI)
- Django Filter
- Environs (`.env` парсинг)
- Faker (генерация тестовых данных)

**Dev / Test:**

- `black`, `flake8`, `isort` — линтинг и форматирование
- `pytest`, `pytest-django`, `pytest-cov` — тесты и покрытие

---

## 🛠 Установка и настройка вручную (без Docker)

### 1. Клонирование проекта

```bash
git clone https://github.com/yourusername/ElectronicsNetwork.git
cd ElectronicsNetwork
```

### 2. Создание и активация виртуального окружения

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate       # Windows
```

### 3. Установка зависимостей через Poetry

```bash
pip install poetry
poetry install
```

### 4. Настройка переменных окружения

Создайте `.env` в корне проекта:

```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 5. Применение миграций

```bash
python manage.py migrate
```

---

## 🚢 Запуск проекта в Docker

### Требования
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 📄 1. Подготовка `.env`

Создай файл `.env` в корне проекта (или используй `.env.example`), например:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_NAME=network
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
```

### ⚙️ 2. Сборка и запуск контейнеров

```bash
docker compose up --build
```

> При первом запуске:
> - будет создана база данных;
> - выполнены миграции;
> - заполнены тестовые данные (`populate_db`, `populate_product_availability`);
> - запустится сервер на http://localhost:8000.

### 🧪 3. Полезные команды

**Повторно применить миграции вручную:**
```bash
docker compose run --rm run_migrations
```

**Повторно заполнить данные:**
```bash
docker compose run --rm init_data
```

**Запустить только web-сервер:**
```bash
docker compose up web
```

### 💡 Примечания

- В `docker-compose.yml` используется многоступенчатый запуск:
  - `db` — база данных PostgreSQL
  - `run_migrations` — миграции при старте
  - `init_data` — заполнение начальных данных **только один раз**
  - `web` — Django-сервер
- Команда запуска определяется через `command:`, **`entrypoint.sh` не используется**.

---

## 🔗 API Endpoints

- `GET /api/network/` — список узлов
- `POST /api/network/` — создать узел
- `GET /api/network/{id}/` — получить узел
- `PUT /api/network/{id}/` — полное обновление
- `PATCH /api/network/{id}/` — частичное обновление
- `DELETE /api/network/{id}/` — удалить узел

### 🔍 Фильтрация и поиск
- `?type=factory`
- `?city=Moscow`
- `?country=Russia`
- `?search=test`

### 📚 Документация API

- Swagger UI: [`/swagger/`](http://localhost:8000/swagger/)

---

## 📦 Модели

### `NetworkNode`
- Тип узла: `factory`, `distributor`, `dealer`, `retail`
- Поставщик (иерархия)
- Контакты, задолженность, дата создания

### `Product`
- Название, модель, дата выхода
- Привязка к узлу

### `ProductAvailability`
- Остатки товара по узлам

---

## ⚙️ Управляющие команды

### Тестовые данные

```bash
python manage.py populate_db
```

### Наличие товаров

```bash
python manage.py populate_product_availability --min-quantity 0 --max-quantity 100
```

---

## 🧪 Тестирование

```bash
pytest
```

Покрытие кода:

```bash
pytest --cov=network
```

---

## 🎯 Стандарты кода

```bash
black .
flake8 .
isort .
```

---

## 📁 Структура проекта

```
ElectronicsNetwork/
├── config/         # Настройки Django
├── network/        # Бизнес-логика приложения
├── manage.py
├── README.md
├── pyproject.toml
├── .env.example
└── .gitignore
```

---

## 📝 Автор

**Evgenii Antonyuk**  
📧 evgeniiantonyuk@gmail.com

---

## 📄 Лицензия

MIT License — свободно для использования и доработки.