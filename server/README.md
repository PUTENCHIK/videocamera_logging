# API сервер VideocameraLogging

## Развёртывание

### 2. Установка зависимостей

Перейти в директорию сервера:
```shell
cd server           # при нахождении в корневой директории проекта
```

Используя `venv` (или другой удобный инструмент), создать виртуальное окружение:
```shell
python -m venv .venv/
```

Активировать созданное окружение.

Для Windows:
```shell
.venv\Scripts\activate
```

Для Linux:
```bash
.venv/bin/activate
```

Установить зависимости Python, указанные в соответствующем файле:
```shell
pip install -r requirements.txt
```

### 3. Запуск сервера

Запустить скрипт в `/server`:
```shell
python main.py
```

Или можно использовать `uvicorn` в консоли (для более гибкой настройки). Сначала удостовериться в существовании папок:

Для Windows:
```shell
if not exist "storage\snapshots" mkdir "storage\snapshots"
if not exist "storage\models" mkdir "storage\models"
```

Для Linux:
```bash
mkdir -p storage/snapshots
mkdir -p storage/models
```

Выполнить:
```shell
uvicorn src.app:app --host=localhost --port=5050 --reload
```
