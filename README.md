# Приложение для логирования объектов с видеокамер

## Развёртывание приложения

### 1.1. Клонирование целиком

Клонирование репозитория целиком, включая предобученные модели из storage/models (более 300МБ):
```shell
git clone https://github.com/PUTENCHIK/videocamera_logging.git
cd videocamera_logging
```

### 1.2. Частичное клонирование
Можно исключить все или часть моделей. Клонирование репозитория без выгрузки файлов:
```shell
git clone --no-checkout https://github.com/PUTENCHIK/videocamera_logging.git
cd videocamera_logging
```

Включение Sparse Checkout и создание файла с шаблонами:
```shell
git config core.sparseCheckout true
type nul > .git/info/sparse-checkout
```

В файл `.git/info/sparse-checkout` необходимо внести все файлы в корне, но исключить директорию с моделями, или только некоторые из них:
```shell
/*
!/storage/yolo11m_100.pt                # игнорируется одна модель
!/storage/*                             # или все модели
```

Выгрузить файлы:
```shell
git checkout
```

Однако при полном исключении всех моделей, или поставленной по умолчанию в поле `Config.model.default` в `src.config`, необходимо заменить на название новой модели, помещённой в директорию `storage/models`.

### 2. Установка зависимостей

Используя `venv` (или другой удобный инструмент), создать виртуальное окружение:
```shell
python -m venv .venv/
```

Активировать созданное окружение:

Для Windows:
```shell
.venv\Scripts\activate
```

Для Linux:
```bash
.venv/bin/activate
```

Установить зависимости Python:
```shell
pip install -r requirements.txt
```

### 3. Запуск приложения

Запустить скрипт в корне проекта:
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

