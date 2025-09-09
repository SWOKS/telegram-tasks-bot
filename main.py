# main.py
import os
import sqlite3
import telebot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден в .env")

bot = telebot.TeleBot(TOKEN)

# --- DB init ---
conn = sqlite3.connect('tasks.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT
)
''')
conn.commit()

def add_task(user_id: int, text: str) -> int:
    cursor.execute('INSERT INTO tasks (user_id, text) VALUES (?, ?)', (user_id, text))
    conn.commit()
    return cursor.lastrowid

def get_tasks(user_id: int):
    cursor.execute('SELECT id, text FROM tasks WHERE user_id = ? ORDER BY id', (user_id,))
    return cursor.fetchall()

def delete_task(user_id: int, task_id: int) -> bool:
    cursor.execute('DELETE FROM tasks WHERE user_id = ? AND id = ?', (user_id, task_id))
    conn.commit()
    return cursor.rowcount > 0

# --- Handlers ---
@bot.message_handler(commands=['start'])
def cmd_start(message):
    txt = ("Привет! Я бот-напоминалка.\n"
           "Команды:\n"
           "/add <текст> — добавить задачу\n"
           "/list — показать задачи\n"
           "/del <id> — удалить задачу\n"
           "/help — подсказка")
    bot.send_message(message.chat.id, txt)

@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.reply_to(message, "Используй /add, /list, /del. Пример: /add Купить хлеб")

@bot.message_handler(commands=['add'])
def cmd_add(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2 or not parts[1].strip():
        bot.reply_to(message, "Напиши текст задачи после /add, например: /add Сделать дз")
        return
    task_text = parts[1].strip()
    add_task(message.from_user.id, task_text)
    bot.reply_to(message, f"Задача добавлена: {task_text}")

@bot.message_handler(commands=['list'])
def cmd_list(message):
    tasks = get_tasks(message.from_user.id)
    if not tasks:
        bot.reply_to(message, "У тебя пока нет задач.")
        return
    resp = "\n".join([f"{tid}. {txt}" for tid, txt in tasks])
    bot.reply_to(message, "Твои задачи:\n" + resp)

@bot.message_handler(commands=['del'])
def cmd_del(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2 or not parts[1].strip().isdigit():
        bot.reply_to(message, "Напиши /del <id>, например: /del 2")
        return
    tid = int(parts[1].strip())
    ok = delete_task(message.from_user.id, tid)
    if ok:
        bot.reply_to(message, f"Задача {tid} удалена.")
    else:
        bot.reply_to(message, "Задача не найдена.")

if __name__ == '__main__':
    print("Bot is running...")
    bot.polling(none_stop=True)
