# Cat Health Tracker

Локальное веб-приложение для мониторинга здоровья кошек.
Запускается на компьютере, открывается в браузере. Один пользователь.

## Архитектура

```
Cat healt/
├── backend/                  # Python + FastAPI
│   ├── alembic/              # Миграции базы данных
│   │   ├── versions/         # Файлы миграций
│   │   ├── env.py            # Конфигурация Alembic
│   │   └── script.py.mako    # Шаблон миграции
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py         # Настройки (pydantic-settings)
│   │   ├── database.py       # SQLAlchemy engine + сессии
│   │   ├── main.py           # Точка входа FastAPI
│   │   ├── models/           # ORM-модели
│   │   │   ├── __init__.py
│   │   │   ├── _mixins.py    # TimestampMixin
│   │   │   ├── animal.py
│   │   │   ├── weight_measurement.py
│   │   │   ├── metric.py
│   │   │   ├── study.py
│   │   │   ├── metric_result.py
│   │   │   ├── document.py
│   │   │   ├── dashboard_settings.py
│   │   │   └── import_history.py
│   │   └── routers/          # API-роутеры (заглушки)
│   ├── alembic.ini
│   └── requirements.txt
├── frontend/                 # React + TypeScript + Vite
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── index.css
│   │   └── vite-env.d.ts
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── uploads/                  # Загруженные документы (PDF, изображения)
├── data/                     # База данных SQLite
├── .env.example
├── .gitignore
└── README.md
```

## Схема базы данных

| Таблица | Описание |
|---------|----------|
| `animals` | Животные: имя, дата рождения, пол, диагнозы, архивный статус |
| `weight_measurements` | Измерения веса (животное, дата, значение в кг) |
| `metrics` | Справочник показателей (название, синонимы, категория, единицы) |
| `studies` | Исследования (животное, даты, тип, лаборатория, комментарий) |
| `metric_results` | Результаты показателей (значение, единица, границы нормы) |
| `documents` | Документы (животное, тип, файл, связь с исследованием) |
| `dashboard_settings` | Настройки дашборда (одна строка, JSON) |
| `import_history` | История импорта (хэш файла — защита от дубликатов) |

### Связи

- `animals` 1:N `weight_measurements` (CASCADE)
- `animals` 1:N `studies` (CASCADE)
- `animals` 1:N `documents` (CASCADE)
- `studies` 1:N `metric_results` (CASCADE)
- `studies` 1:N `documents` (SET NULL при удалении исследования)
- `metrics` 1:N `metric_results` (RESTRICT — нельзя удалить показатель с результатами)

## Требования

- Python 3.11+
- Node.js 18+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (для OCR)

## Установка и запуск

### 1. Настройка окружения

```bash
# Скопируйте пример конфигурации
cp .env.example .env          # Linux/Mac
copy .env.example .env        # Windows
```

Отредактируйте `.env` при необходимости (путь к Tesseract, порт и т.д.).

### 2. Backend

```bash
cd backend

# Создайте виртуальное окружение
python -m venv .venv

# Активация
.venv\Scripts\activate          # Windows (PowerShell)
# source .venv/bin/activate     # Linux/Mac

# Установка зависимостей
pip install -r requirements.txt

# Создание первой миграции и применение
alembic revision --autogenerate -m "initial schema"
alembic upgrade head

# Запуск сервера
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend: `http://127.0.0.1:8000`
Swagger UI: `http://127.0.0.1:8000/docs`

### 3. Frontend

В отдельном терминале:

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev-сервера
npm run dev
```

Frontend: `http://localhost:5173`

Vite настроен с прокси: запросы к `/api/*` автоматически перенаправляются на backend (`127.0.0.1:8000`).

## Текущее состояние

Реализована структура проекта, модели данных и конфигурация.  
Бизнес-логика (API-роутеры, OCR-импорт, графики) добавляется на следующих этапах.

## Стек

- **Backend**: Python, FastAPI, SQLite, SQLAlchemy 2.0, Alembic
- **Frontend**: React, TypeScript, Vite
- **Графики**: Recharts
- **PDF**: PyMuPDF, pdfplumber
- **OCR**: Tesseract (pytesseract + pdf2image)
