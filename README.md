# ms-bot-python

Музыкальный бот для Discord сервера.

## Команды

Умеет обрабатывать текстовые команды (например, `%инфо`) и Splash (через `/` в начале чата):

<img width="531" height="603" alt="Скриншот информативной команды" src="https://github.com/user-attachments/assets/219bf80f-a661-4550-a60a-b4bee758466f" />

## Запуск проекта

Поставьте и запустите окружение:

```bash
python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # Linux/macOS
```

Установите зависимости из файла:

```bash
pip install -r requirements.txt
```

Настройки конфигурационный файл:

```bash
cp .env.example .env
```

Запустите бота:

```bash
python bot.py
```

## Требования

Для работы проигрывателя установите [FFmpeg](https://www.ffmpeg.org/).
