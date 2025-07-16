import telebot
import sqlite3

bot = telebot.TeleBot('8140677544:AAFZzTOBYZyb_vUEJyh0m9J14n4OIlvJfts')
set_id = None

@bot.message_handler(commands=['start'])
def start(message):
    str
    check_id = str(message.text[6:])
    if str(check_id) !="":
        conn = sqlite3.connect('scripts.sql')
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM scripts WHERE id = {check_id}')
        info = cur.fetchone()
        if info is None:
            bot.send_message(message.chat.id, f'⛔️ <b>Код скрипта:{check_id} не найден в базе данных!</b>\n\n<i>❓ Если вы думаете что это ошибка обратитесь к владельцу: @wavyjzw</i>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, f'📃 <b>Текущий код скрипта: {check_id}</b>', parse_mode='html')
            bot.send_message(message.chat.id, f'{info[1]}\n\n🤍 Лучшие скрипты: @sadlunovSCRIPTS', parse_mode='html')

            cur.close()
            conn.close()
    else:
        bot.send_message(message.chat.id, '🤍 <b>Привет! Ты запустил бота созданный для канала @sadlunovSCRIPTS</b>\n\n📃 <i>Если у тебя появились вопросы то ты можешь обратиться к создателю данного бота: @wavyjzw</i>', parse_mode='html')

@bot.message_handler(commands=['set'])
def start(message):
    conn = sqlite3.connect('scripts.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS scripts (id	INTEGER NOT NULL UNIQUE, script TEXT NOT NULL)')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, '❔<i>Придумайте айди:</i>', parse_mode='html')
    bot.register_next_step_handler(message, get_id)


def get_id(message):
    global set_id
    set_id = message.text.strip()
    bot.send_message(message.chat.id, '❔<i>Отправьте скрипт:</i>', parse_mode='html')
    bot.register_next_step_handler(message, get_script)

def get_script(message):
    set_script = message.text.strip()

    conn = sqlite3.connect('scripts.sql')
    cur = conn.cursor()

    cur.execute(f'INSERT INTO scripts (id, script) VALUES ("%s", "%s")' % (set_id, set_script))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, '📃 <b>Скрипт успешно записан в базу данных!</b>', parse_mode='html')


bot.polling(none_stop=True)