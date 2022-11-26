from telebot import TeleBot as tebot_TeleBot
from json import load as js_load, dump as js_dump, dumps as js_dumps
from requests import get as req_get, put as req_put, exceptions as req_exceptions
from time import mktime as time_mktime, sleep as time_sleep
from datetime import datetime, timedelta
from os import environ as os_environ

token = os_environ.get('TOKEN')
bot = tebot_TeleBot(token)

while True:
    try:
        time_now = req_get('http://worldtimeapi.org/api/timezone/Europe/Moscow', timeout=3)
    except req_exceptions.Timeout:
        print('connection timeout: http://worldtimeapi.org/api/timezone/Europe/Moscow')
        time_sleep(10)
        continue

    time_now = datetime.strptime(time_now.json()['utc_datetime'], '%Y-%m-%dT%H:%M:%S.%f+00:00').replace(microsecond=0, second=0)
    time_now = int(time_mktime(time_now.timetuple()))
    try:
        req_in_db = req_get('http://192.168.3.38:5000/notif_list', timeout=3)
    except req_exceptions.RequestException:
        print('connection timeout: api/notif_list')
        time_sleep(10)
        continue

    for obj in req_in_db.json():
        if obj['time'] == time_now:
            bot.send_message(obj['id_user'], obj['text'])
            try: 
                req_del_notif = req_put('http://192.168.3.38:5000/del_notif', headers={'Content-Type': 'application/json'}, data=js_dumps(obj), timeout=3)
            except req_exceptions.RequestException:
                print('connection timeout: api/del_notif')
            print(req_del_notif.status_code)
            print(req_del_notif.text)

    time_sleep(5)
