#>cd projects\pythonprojects\myweatherbot\myweatherbot\bot
#https://t.me/joinchat/AAAAAFfzbHvR_9TAg_DzPg
import sys
import json
import bot_api
import time
import telebot
import datetime
from GetterAPI.get_api import get
from threading import Thread

CHANNEL_NAME = '@gusarov2906_channel'

bot = bot_api.create_bot()

def fix_wd(i):
    if (i==7):
        i=0
    #print(f"ok, ret {i}")
    return i

def get_data_from_file_cur():
    try:
        with open("data_cur_weather.json",'r',encoding='utf-8') as file:
                f = json.load(file)

                weather_status = f['weather'][0]['main']
                weather_description = f['weather'][0]['description']

                cur_temp = f['main']['temp']
                cur_temp_min = f['main']['temp_min']
                cur_temp_max = f['main']['temp_max']
                feels_like = f['main']['feels_like']
                pressure = f['main']['pressure']
                humidity = f['main']['humidity']
                location = f['name']

                weather_message = f"\n Описание: {weather_description} \n Текущая температура: {cur_temp} ℃ \n Максимальная температура: {cur_temp_max} ℃ \n Минимальная температура: {cur_temp_min} ℃ \n Ощущается как: {feels_like} ℃\n Давление: {humidity} hPa\n Влажность: {humidity} %"
        return weather_message,location
    except Exception as e:
        print("Exception: ", e)
        pass

def get_data_from_file_forecast(weekday_today):
    try:
        with open("data_forecast.json",'r',encoding='utf-8') as file:
            f = json.load(file)
            weather_message = []
            weather_message_forecast=[]
            weather_message_today=[]
            weather_message_tomorrow=[]

            last_date = ""
            i = 0
            new_weekday = weekday_today
            for item in f['list']:
                #print(f"\n{item}\n")
                date = item['dt_txt']
                weather_description = item['weather'][0]['description']
                cur_temp = item['main']['temp']

                if ("9:" in date)or("15:" in date)or("21:" in date)or("3:"in date):
                    if (last_date[0:10]!=date[0:10]):
                        new_weekday = fix_wd(new_weekday+i)
                        weather_message_forecast.append(f"\nПрогноз на {days[new_weekday]} ({date[0:10]})\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃")
                        i=1
                    else:
                        weather_message_forecast.append(f"Время: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃")
                    last_date = date
            i = 0
            for item in f['list']:
                date = item['dt_txt']
                weather_description = item['weather'][0]['description']
                cur_temp = item['main']['temp']
                cur_temp_min = item['main']['temp_min']
                cur_temp_max = item['main']['temp_max']
                feels_like = item['main']['feels_like']
                pressure = item['main']['pressure']
                humidity = item['main']['humidity']

                if ((datetime.date.today() + datetime.timedelta(days=1)).strftime("%d")==date[8:10]):
                    if (i==0):
                        #weather_message_today.append(f"\nПрогноз на сегодня ({date[0:10]})\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Максимальная температура: {cur_temp_max} ℃ \n Минимальная температура: {cur_temp_min} ℃ \n Ощущается как: {feels_like} ℃\n Давление: {humidity} hPa\n Влажность: {humidity} %")
                        weather_message_tomorrow.append(f"\nПрогноз на завтра ({date[0:10]})\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Ощущается как: {feels_like} ℃\n Влажность: {humidity} %")
                        i=1
                    else:
                        #weather_message_today.append(f"\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Максимальная температура: {cur_temp_max} ℃ \n Минимальная температура: {cur_temp_min} ℃ \n Ощущается как: {feels_like} ℃\n Давление: {humidity} hPa\n Влажность: {humidity} %")
                        weather_message_tomorrow.append(f"\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Ощущается как: {feels_like} ℃ \n Влажность: {humidity} %")

            i = 0
            for item in f['list']:
                date = item['dt_txt']
                weather_description = item['weather'][0]['description']
                cur_temp = item['main']['temp']
                cur_temp_min = item['main']['temp_min']
                cur_temp_max = item['main']['temp_max']
                feels_like = item['main']['feels_like']
                pressure = item['main']['pressure']
                humidity = item['main']['humidity']

                if (datetime.datetime.today().strftime("%d")==date[8:10]):
                    if (i==0):
                        #weather_message_today.append(f"\nПрогноз на сегодня ({date[0:10]})\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Максимальная температура: {cur_temp_max} ℃ \n Минимальная температура: {cur_temp_min} ℃ \n Ощущается как: {feels_like} ℃\n Давление: {humidity} hPa\n Влажность: {humidity} %")
                        weather_message_today.append(f"\nПрогноз на сегодня ({date[0:10]})\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Ощущается как: {feels_like} ℃\n Влажность: {humidity} %")
                        i=1
                    else:
                        #weather_message_today.append(f"\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Максимальная температура: {cur_temp_max} ℃ \n Минимальная температура: {cur_temp_min} ℃ \n Ощущается как: {feels_like} ℃\n Давление: {humidity} hPa\n Влажность: {humidity} %")
                        weather_message_today.append(f"\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Ощущается как: {feels_like} ℃ \n Влажность: {humidity} %")
            weather_message.append(weather_message_forecast)
            weather_message.append(weather_message_today)
            weather_message.append(weather_message_tomorrow)
            return weather_message

    except Exception as e:
        print("Exception: ", e)
        pass

def sending_morning_mes(bot,message):
    now = datetime.datetime.now()
    year = int(now.strftime("%Y"))
    month = int(now.strftime("%m"))
    day = int(now.strftime("%d"))
    hours = int(now.strftime("%H"))
    minutes = int(now.strftime("%M"))
    if (hours >= 9):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        day = int(tomorrow.strftime("%d"))
    t_time = datetime.datetime(year,month,day,9,0)
    print(t_time)
    print(now)
    print((t_time -now).seconds)
    time.sleep((t_time -now).seconds)
    get()
    weather_messages = []
    weather_message = "Доброе утро!)"
    weather_messages = get_data_from_file_forecast(weekday_today)
    for item in weather_messages[1]:
        weather_message = weather_message + "\n" + item
    bot.send_message(message.chat.id,weather_message)
    while(True):
        time.sleep(86400)
        get()
        weather_message = ""
        weather_message = "Доброе утро!)"
        weather_messages = get_data_from_file_forecast(weekday_today)
        for item in weather_messages[1]:
            weather_message = weather_message + "\n" + item
        bot.send_message(message.chat.id,weather_message)

def sending_evening_mes(bot,message):
    now = datetime.datetime.now()
    year = int(now.strftime("%Y"))
    month = int(now.strftime("%m"))
    day = int(now.strftime("%d"))
    hours = int(now.strftime("%H"))
    minutes = int(now.strftime("%M"))
    if (hours >= 21):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        day = int(tomorrow.strftime("%d"))
    t_time = datetime.datetime(year,month,day,21,00)
    print(t_time)
    print(now)
    print((t_time -now).seconds)
    time.sleep((t_time -now).seconds)
    get()
    weather_message = "Добрый вечер!)"
    weather_messages = get_data_from_file_forecast(weekday_today)
    for item in weather_messages[2]:
        weather_message = weather_message + "\n" + item
    bot.send_message(message.chat.id,weather_message)
    while(True):
        time.sleep(86400)
        get()
        weather_messages = []
        weather_message = ""
        weather_messages = get_data_from_file_forecast(weekday_today)
        for item in weather_messages[2]:
            weather_message = weather_message + "\n" + item
        bot.send_message(message.chat.id,weather_message)
#main


today = datetime.datetime.today()
now = datetime.datetime.now()
weekday_today = datetime.date.weekday(today)
days= ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

get()
get_data_from_file_forecast(weekday_today)
weather_message,location = get_data_from_file_cur()

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Погода сейчас', 'Погода сегодня','Погода завтра','Прогноз погоды')


sending_flag = True

#@bot.message_handler(commands=['change_notifications'])
#def send_text(message):
#    print(sending_flag)
#    if(sending_flag):
#        th1 = Thread(target=sending_morning_mes, name="Thread0",args = (bot,message), daemon = True)
#        th2 = Thread(target=sending_evening_mes, name="Thread1",args = (bot,message), daemon = True)
#        th1.start()
#        th2.start()
#    else:
#    print("threading not work")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Привет, ты написал мне /start\nЭто бот мониторинга погоды\nВ данный момент локация погоды: {location}\n Для настроки уведолений зайдите в настройки /settings\n', reply_markup=keyboard1)
    if(sending_flag):
        th1 = Thread(target=sending_morning_mes, name="Thread0",args = (bot,message), daemon = True)
        th2 = Thread(target=sending_evening_mes, name="Thread1",args = (bot,message), daemon = True)
        th1.start()
        th2.start()

@bot.message_handler(commands=['settings'])
def send_text(message):
    bot.send_message(message.chat.id, f'Настройки: \n   ')

#@bot.message_handler(commands=['notification'])
#def send_text(message):
#    markup = telebot.types.InlineKeyboardMarkup()
#    markup.add(telebot.types.InlineKeyboardButton(text='Включить', callback_data=1))
#    markup.add(telebot.types.InlineKeyboardButton(text='Выключить', callback_data=2))
#    bot.send_message(message.chat.id, text="Отправка уведомлений о погоде с утра и вечером", reply_markup=markup)

#@bot.callback_query_handler(func=lambda call: True)
#def query_handler(call,sending_flag):
#    bot.answer_callback_query(callback_query_id=call.id, text='Изменения приняты')
#    answer = ''
#    if call.data == '1':
#        answer = 'Изменения приняты+'
#        sending_flag = True

#    elif call.data == '2':
#        answer = 'Изменения приняты-'
#        sending_flag = False
#
#    bot.send_message(call.message.chat.id, answer)
#    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=['text'])
def send_text(message):
    today = datetime.datetime.today()
    now = datetime.datetime.now()
    weekday_today = datetime.date.weekday(today)
    get()

    if message.text == 'Погода сейчас':
        weather_message =f'Сейчас: {now.strftime("%x")} {now.strftime("%X")}'
        tmp,location = get_data_from_file_cur()
        weather_message += tmp
        bot.send_message(message.chat.id,weather_message)

    if message.text == 'Прогноз погоды':
        weather_messages = []
        weather_message = ""
        weather_messages = get_data_from_file_forecast(weekday_today)
        last_item = weather_messages[0][0]
        for item in weather_messages[0]:
            weather_message = weather_message + "\n" + item
            last_item = item
        bot.send_message(message.chat.id,weather_message)

    if message.text == 'Погода сегодня':
        weather_messages = []
        weather_message = ""
        weather_messages = get_data_from_file_forecast(weekday_today)
        for item in weather_messages[1]:
            weather_message = weather_message + "\n" + item
        bot.send_message(message.chat.id,weather_message)

    if message.text == 'Погода завтра':
        weather_messages = []
        weather_message = ""
        weather_messages = get_data_from_file_forecast(weekday_today)
        for item in weather_messages[2]:
            weather_message = weather_message + "\n" + item
        bot.send_message(message.chat.id,weather_message)


bot.polling()

#    with open("data_weather.txt",'r') as file:
#            f = file.read()
#            print(f)
