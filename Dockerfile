# Используем официальный образ Python 3.13
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем зависимости
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости проекта без создания venv
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root --no-interaction --no-ansi

# Копируем весь проект
COPY . .

