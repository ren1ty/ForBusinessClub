import telebot
import sqlite3
from telebot import types
from datetime import datetime

bot = telebot.TeleBot('6699548657:AAFYwFkJb7reOIwPuHfHZmqnyzIfLDC39xg')

conn = sqlite3.connect('user_actions.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  user_id INTEGER PRIMARY KEY,
                  last_activity TEXT)''')
conn.commit()


def db_exec(query, *params):
    conn = sqlite3.connect('user_actions.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    return result

@bot.message_handler(commands=['admin'])
def handle_admin(message):
    user_id = message.chat.id
    count = db_exec("SELECT COUNT(user_id) FROM users")[0][0]
    print(count)
    bot.send_message(user_id, f"Количество пользователей в боте: {count}")

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    current_time = datetime.now().strftime('%Y:%m:%d %H:%M:%S')
    db_exec("INSERT OR REPLACE INTO users (user_id, last_activity) VALUES (?, ?)", user_id, current_time)

    markup = types.ReplyKeyboardMarkup()
    admin_button = types.KeyboardButton('/admin')
    markup.row(admin_button)

    bot.send_message(user_id, "Привет! Я был разработан для отбора в бизнес клуб Вышки", reply_markup=markup)

bot.infinity_polling()

