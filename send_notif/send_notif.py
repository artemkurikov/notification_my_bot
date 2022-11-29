from telebot import TeleBot as tebot_TeleBot
from json import load as js_load, dump as js_dump, dumps as js_dumps
from requests import get as req_get, put as req_put, exceptions as req_exceptions
from time import mktime as time_mktime, sleep as time_sleep
from datetime import datetime, timedelta
from toml import load as toml_load

with open('conf/config.toml', 'r') as file:
    config = toml_load(file)

token = config['conf']['token']
ip = config['conf']['ip']
port = config['conf']['port']
bot = tebot_TeleBot(token)

while True:
    try:
        time_now = req_get('http://worldtimeapi.org/api/timezone/Europe/Moscow', timeout=5)
    except req_exceptions.RequestException:
        print('connection timeout: http://worldtimeapi.org/api/timezone/Europe/Moscow')
        continue
    time_now = datetime.strptime(time_now.json()['utc_datetime'], '%Y-%m-%dT%H:%M:%S.%f+00:00').replace(microsecond=0, second=0)
    time_now = int(time_mktime(time_now.timetuple()))
    try:
        req_in_db = req_get(f'http://{ip}:{port}/notif_list', timeout=3)
    except req_exceptions.RequestException:
        print('connection timeout: api/notif_list')
        time_sleep(10)
        continue

    for lists in req_in_db.json():
        if lists.count(time_now):
            bot.send_message(lists[1], lists[2])
            try: 
                req_del_notif = req_put(f'http://{ip}:{port}/del_notif', headers={'Content-Type': 'application/json'}, data=js_dumps(lists), timeout=3)
            except req_exceptions.RequestException:
                print('connection timeout: api/del_notif')
            print(req_del_notif.status_code)
            print(req_del_notif.text)

    time_sleep(5)

