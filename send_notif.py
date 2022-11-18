import telebot
from json import load as js_load, dump as js_dump, dumps as js_dumps
from requests import get as req_get, put as req_put
import time
from datetime import datetime, timedelta
import os

token = os.environ.get('TOKEN')
bot = telebot.TeleBot(token)

while True:
    time_now = req_get('http://worldtimeapi.org/api/timezone/Europe/Moscow')
    time_now = datetime.strptime(time_now.json()['utc_datetime'], '%Y-%m-%dT%H:%M:%S.%f+00:00').replace(microsecond=0, second=0)
    time_now = int(time.mktime(time_now.timetuple()))
    req_in_db = req_get('http://192.168.3.38:5000/notif_list')

    for obj in req_in_db.json():
        if obj['time'] == time_now:
            bot.send_message(obj['id_user'], obj['text'])
            req_del_notif = req_put('http://192.168.3.38:5000/del_notif', headers={'Content-Type': 'application/json'}, data=js_dumps(obj))
            print(req_del_notif.status_code)
            print(req_del_notif.text)

    time.sleep(5)

