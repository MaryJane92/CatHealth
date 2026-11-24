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

## Установка и запуск — пошаговая инструкция

Ниже — детальная инструкция для Windows (PowerShell). Команды для Linux/Mac указаны в комментариях.

### Предварительные требования

Перед началом установите три программы:

| Программа | Минимальная версия | Где скачать |
|-----------|-------------------|-------------|
| **Python** | 3.11+ | https://www.python.org/downloads/ |
| **Node.js** | 18+ (LTS) | https://nodejs.org/ |
| **Tesseract OCR** | любая | https://github.com/UB-Mannheim/tesseract/wiki |

**Важно при установке:**
- Python: при установке отметьте галочку **«Add Python to PATH»**.
- Node.js: при установке отметьте **«Add to PATH»**.
- Tesseract: запомните путь установки — по умолчанию `C:\Program Files\Tesseract-OCR\`.

**Проверка установки** — откройте PowerShell и выполните:

```powershell
python --version      # должно вывести: Python 3.11.x или выше
node --version        # должно вывести: v18.x.x или выше
npm --version         # должно вывести: 9.x.x или выше
```

Если хотя бы одна команда не распознана — перезапустите PowerShell после установки и проверьте снова.

---

### Шаг 1. Подготовка конфигурации

Откройте PowerShell в папке проекта (`d:\Cat healt`) и скопируйте файл настроек:

```powershell
Copy-Item .env.example .env
```

Откройте файл `.env` в любом текстовом редакторе. Проверьте строку `TESSERACT_CMD`:

```
# Если Tesseract установлен по стандартному пути — раскомментируйте строку:
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

# Если Tesseract добавлен в PATH — можно оставить пустым:
TESSERACT_CMD=
```

Остальные значения можно не менять — они настроены для локальной работы по умолчанию.

---

### Шаг 2. Установка зависимостей Backend

```powershell
# 1. Перейдите в папку backend
cd backend

# 2. Создайте виртуальное окружение
python -m venv .venv

# 3. Активируйте виртуальное окружение
.\.venv\Scripts\Activate.ps1
# После активации в начале строки появится префикс: (.venv)

# Если появилась ошибка "выполнение сценариев отключено" — выполните:
#   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# и повторите активацию.

# 4. Установите зависимости
pip install -r requirements.txt
# Этот шаг займёт 1–3 минуты. Дождитесь сообщения "Successfully installed ...".

# 5. Проверьте, что FastAPI установлен
python -c "import fastapi; print('FastAPI', fastapi.__version__)"
# Должно вывести: FastAPI 0.115.6
```

---

### Шаг 3. Создание базы данных

База данных создаётся через миграции Alembic. Виртуальное окружение должно быть активно (см. шаг 2).

```powershell
# Находитесь в папке backend, виртуальное окружение активно

# 1. Создайте миграцию на основе моделей
alembic revision --autogenerate -m "initial schema"

# 2. Примените миграцию — создаст файл SQLite и таблицы
alembic upgrade head

# 3. Проверьте, что файл БД создан
ls ..\data\cat_health.db
# Должен существовать файл cat_health.db
```

**Если что-то пошло не так:**
- Ошибка `Target database is not up to date` → выполните `alembic upgrade head` ещё раз.
- Ошибка `Can't locate revision` → удалите папку `data/` целиком, удалите все файлы в `backend/alembic/versions/` и повторите шаг 3 с начала.

---

### Шаг 4. Запуск Backend

```powershell
# Находитесь в папке backend, виртуальное окружение активно

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Признак успеха:** в консоли появится:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**Проверка:** откройте в браузере:
- http://127.0.0.1:8000/docs — откроется Swagger UI с списком endpoints.
- http://127.0.0.1:8000/ — должен вернуть базовый ответ.

**Не закрывайте этот терминал.** Backend должен работать во время использования приложения.

---

### Шаг 5. Установка зависимостей Frontend

Откройте **новое окно PowerShell** (отдельно от backend).

```powershell
# 1. Перейдите в папку проекта, затем в frontend
cd "d:\Cat healt\frontend"

# 2. Установите зависимости
npm install
# Этот шаг займёт 1–2 минуты. Дождитесь завершения без ошибок.
```

---

### Шаг 6. Запуск Frontend

В том же окне PowerShell, где выполняли шаг 5:

```powershell
npm run dev
```

**Признак успеха:** в консоли появится:

```
  VITE v6.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

**Проверка:** откройте в браузере http://localhost:5173 — приложение должно загрузиться.

Vite настроен с прокси: запросы к `/api/*` автоматически перенаправляются на backend (`127.0.0.1:8000`).

---

### Шаг 7. Проверка работы

1. Backend запущен (терминал 1) — Swagger UI доступен на http://127.0.0.1:8000/docs.
2. Frontend запущен (терминал 2) — интерфейс доступен на http://localhost:5173.
3. Откройте http://localhost:5173 в браузере — приложение должно работать.

Для остановки приложения нажмите `Ctrl+C` в обоих терминалах.

---

### Шаг 8. Последующий запуск (каждый день)

После первой установки повторять шаги 1–3 не нужно. Для запуска:

**Терминал 1 — Backend:**
```powershell
cd "d:\Cat healt\backend"
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Терминал 2 — Frontend:**
```powershell
cd "d:\Cat healt\frontend"
npm run dev
```

---

## Решение частых проблем

| Проблема | Решение |
|----------|---------|
| `python: Имя не распознано` | Python не добавлен в PATH. Переустановите с галочкой «Add Python to PATH» или добавьте путь вручную в переменные среды. |
| `npm: Имя не распознано` | Node.js не добавлен в PATH. Переустановите с галочкой «Add to PATH». Перезапустите PowerShell. |
| `выполнение сценариев отключено` при активации venv | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `pip install` завершается с ошибкой | Обновите pip: `python -m pip install --upgrade pip`, затем повторите установку. |
| `alembic: Имя не распознано` | Виртуальное окружение не активировано. Выполните `.\.venv\Scripts\Activate.ps1` в папке `backend`. |
| `Port 8000 already in use` | Другой процесс занял порт. Запустите на другом: `uvicorn app.main:app --reload --port 8001`. |
| Frontend открывается, но данные не загружаются | Backend не запущен. Проверьте, что в терминале 1 работает `uvicorn`. |
| OCR не работает (ошибка Tesseract) | Укажите путь в `.env`: `TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe` |
| База данных пустая после перезапуска | Проверьте, что файл `data/cat_health.db` существует. Если удалён — повторите шаг 3. |

## Текущее состояние

Реализована структура проекта, модели данных и конфигурация.  
Бизнес-логика (API-роутеры, OCR-импорт, графики) добавляется на следующих этапах.

## Стек

- **Backend**: Python, FastAPI, SQLite, SQLAlchemy 2.0, Alembic
- **Frontend**: React, TypeScript, Vite
- **Графики**: Recharts
- **PDF**: PyMuPDF, pdfplumber
- **OCR**: Tesseract (pytesseract + pdf2image)
