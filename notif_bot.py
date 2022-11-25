import telebot
from re import search as re_search
from json import dump as js_dump, load as js_load, dumps as js_dumps
from datetime import datetime, timedelta
from time import mktime, sleep as tm_sleep
from requests import post as req_post
from os import environ as os_environ

token = os_environ.get('TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def text_messages(message):
    notif_obj = {}
    if re_search(r'\\set \d\d:\d\d \d\d\.\d\d.\d\d \w.*', message.text):
        notif_obj['id_user'] = message.from_user.id
        new_time = datetime.strptime(re_search(r'\d\d:\d\d \d\d.\d\d.\d\d', message.text).group(0), '%H:%M %d.%m.%y') - timedelta(hours=3)
        notif_obj['time'] = int(mktime(new_time.timetuple()))
        notif_obj['text'] = re_search(r'[A-Za-zА-Яа-я].*', message.text[4:]).group(0)
        
        req_add_notif = req_post('http://localhost:5000/new_notif', headers={'Content-Type': 'application/json'}, data=js_dumps(notif_obj))
        print(req_add_notif.status_code)

        bot.send_message(message.from_user.id, 'Напоминание установлено!')
    elif message.text == '/help':
        bot.send_message(message.from_user.id, "Чтобы установить напоминание напишетe: \set hh:mm dd:mm:yy 'text'")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)
