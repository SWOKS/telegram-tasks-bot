# Telegram Tasks Bot

Простой Telegram-бот для заметок/задач (Python + SQLite).

## Команды
- `/add <текст>` — добавить задачу
- `/list` — список задач
- `/del <id>` — удалить задачу

## Как запустить локально
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Создать `.env` с `TELEGRAM_TOKEN=твой_токен`
5. `python main.py`
