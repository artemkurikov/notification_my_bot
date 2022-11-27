import telebot
from re import search as re_search
from json import dump as js_dump, load as js_load, dumps as js_dumps
from datetime import datetime, timedelta
from time import mktime, sleep as tm_sleep
from requests import post as req_post, get as req_get
from os import environ as os_environ

token = os_environ.get('TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['reg'])
def reg(message):
    msg = bot.send_message(message.from_user.id, "input: your gmt \nexamaple: gmt +3")
    bot.register_next_step_handler(msg, get_gmt)

@bot.message_handler(content_types=['text'])
def text_messages(message):
#    if message.text == '/reg':
#        msg = bot.send_message(message.from_user.id, "input: your gmt \nexamaple: gmt +3")
#        bot.register_next_step_handler(msg, get_gmt)
    req_check_user = req_get(f'http://localhost:5000/user/{message.from_user.id}')
    print(req_check_user.json())
    if req_check_user.json().count(0):
        bot.send_message(message.from_user.id, "User not registered!, Please /reg")
        return 0
    notif_list = []
    if re_search(r'\\set \d\d:\d\d (\d\d\.\d\d.\d\d|today|) \w.*', message.text):
        new_time = datetime.strptime(re_search(r'\d\d:\d\d \d\d.\d\d.\d\d', message.text).group(0), '%H:%M %d.%m.%y') - timedelta(hours=3)
        notif_list.append(int(mktime(new_time.timetuple())))
        notif_list.append(message.from_user.id)
        notif_list.append(re_search(r'[A-Za-zА-Яа-я].*', message.text[4:]).group(0))
        
        req_add_notif = req_post('http://localhost:5000/new_notif', headers={'Content-Type': 'application/json'}, data=js_dumps(notif_list))
        print(req_add_notif.status_code)

        bot.send_message(message.from_user.id, 'Напоминание установлено!')
    elif message.text == '/help':
        print(message.date)
        bot.send_message(message.from_user.id, "Чтобы установить напоминание напишетe: \set hh:mm dd:mm:yy 'text'")
#    elif message.text == '/reg':
#        bot.send_message(message.from_user.id, "input: your gmt \nexamaple: gmt +3")
#        bot.register_next_step_handler(message, get_gmt)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

def get_gmt(message):
    if re_search(r'gmt (\+|\-)(\s|)\d.*', message.text):
        gmt_mark = re_search(r'\+|\-', message.text).group(0)
        gmt_numeric = int(re_search(r'(\d.*)', message.text).group(0))
        user_data = [message.from_user.id, gmt_mark, gmt_numeric]
        req_reg = req_post('http://localhost:5000/user_regist', headers={'Content-Type': 'application/json'}, data=js_dumps(user_data))
        bot.send_message(message.from_user.id, "You have successfully registered!")
        return 0

bot.polling(none_stop=True, interval=0)
