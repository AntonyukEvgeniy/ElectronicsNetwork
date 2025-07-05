# Electronics Network

📦 **Electronics Network** — это веб-приложение на Django, моделирующее иерархическую сеть поставщиков в сфере продажи электроники. Приложение предоставляет API и административную панель для управления узлами сети, их поставщиками, продуктами и задолженностями.

## 🔧 Функциональность

- Иерархическая структура из трёх уровней: завод, розничная сеть, индивидуальный предприниматель.
- Каждый узел ссылается только на одного поставщика.
- CRUD-операции через API (на DRF) для узлов сети.
- Поддержка фильтрации по стране в API.
- Django admin:
  - просмотр объектов;
  - фильтр по городу;
  - ссылка на поставщика;
  - admin action для обнуления задолженности.

## 🧱 Технологии

- Python 3.11+
- Django 4.x
- Django REST Framework
- PostgreSQL
- Django Admin

## 🚀 Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/electronics_network.git
   cd electronics_network
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Настройте `.env` файл (если используется):
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgres://user:password@localhost:5432/electronics_db
   ```

4. Примените миграции:
   ```bash
   python manage.py migrate
   ```

5. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

6. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

## 🔐 Авторизация

Доступ к API имеют только **активные сотрудники** (`is_active=True`, `is_staff=True`). Аутентификация по токену или сессии (в зависимости от настройки проекта).

## 🔗 API

- `/api/nodes/` — CRUD для узлов сети (поставщиков).
- Поле `debt_to_supplier` (задолженность) доступно только для чтения.
- Фильтрация по стране:  
  ```http
  GET /api/nodes/?country=Russia
  ```

## 🛠 Примеры моделей

**Узел сети (`NetworkNode`)**
- name
- email, country, city, street, house_number
- supplier (ForeignKey на себя)
- debt_to_supplier (Decimal)
- created_at (auto_now_add)

**Продукт (`Product`)**
- name
- model
- release_date
- network_node (ForeignKey)

## 📂 Структура проекта

```
electronics_network/
├── manage.py
├── config/
│   └── settings.py
├── network/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── admin.py
│   └── urls.py
└── pyproject.toml
```

## ✅ TODO

- [ ] Модели с самоссылкой
- [ ] Admin-интерфейс с action и фильтрами
- [ ] DRF API с ограничением доступа
- [ ] Тесты (Unit/API)
- [ ] Docker-сборка (опционально)

## 📝 Лицензия

MIT License

---

> Разработано в рамках учебного проекта по Django.