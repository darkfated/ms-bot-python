# ms-bot-python

Музыкальный бот для Discord сервера.

## Команды

Умеет обрабатывать текстовые команды (например, `%инфо`) и Splash (через `/` в начале чата):

<img width="710" height="292" alt="image" src="https://github.com/user-attachments/assets/048dcc46-ed06-42c6-982d-808f21d646a7" />

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
