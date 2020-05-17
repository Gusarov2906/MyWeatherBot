#>cd projects\pythonprojects\myweatherbot\myweatherbot\bot
#@gusarov2906_weather_bot

#IMPORTS
import json
import bot_api
import time
import telebot
from telebot import types
import datetime
import threading
from GetterAPI.get_api import get_current_weather
from GetterAPI.get_api import get_forecast_weather
from threading import Thread
import sqlite3



#CONSTANTS
days= ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

#FUNCTIONS
#fix week day(if it equals 7 it means that is first weekday, which equals 0)
def fix_wd(i):
    if (i==7):
        i=0
    return i
flag_to_end = False
#function to get data from files in current directory
def get_from_file(file_name):
    #gets date for current weather message
    if (file_name=="now"):
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
            return weather_message
        except Exception as e:
            print("Exception: ", e)
            with open("error.txt",'w',encoding='utf-8') as file:
                file.write(str(e))
            pass

    #gets data for 5 days forecast weather and return message
    elif (file_name=="week_forecast"):
        try:
            with open("data_forecast.json",'r',encoding='utf-8') as file:
                f = json.load(file)
                weather_message_forecast=[]
                #+  because on location where will live bot not local time
                today = datetime.datetime.today()
                weekday_today = datetime.date.weekday(today)
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
                return weather_message_forecast
        except Exception as e:
                print("Exception: ", e)
                with open("error.txt",'w',encoding='utf-8') as file:
                    file.write(str(e))
                pass

    #gets data tomorrow forecast weather and return message
    elif (file_name=="tomorrow_forecast"):
        try:
            with open("data_forecast.json",'r',encoding='utf-8') as file:
                f = json.load(file)
                weather_message_tomorrow=[]
                isFirst = True
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
                        if isFirst:
                            #weather_message_today.append(f"\nПрогноз на сегодня ({date[0:10]})\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Максимальная температура: {cur_temp_max} ℃ \n Минимальная температура: {cur_temp_min} ℃ \n Ощущается как: {feels_like} ℃\n Давление: {humidity} hPa\n Влажность: {humidity} %")
                            weather_message_tomorrow.append(f"\nПрогноз на завтра ({date[0:10]})\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Ощущается как: {feels_like} ℃\n Влажность: {humidity} %")
                            isFirst = False
                        else:
                            #weather_message_today.append(f"\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Максимальная температура: {cur_temp_max} ℃ \n Минимальная температура: {cur_temp_min} ℃ \n Ощущается как: {feels_like} ℃\n Давление: {humidity} hPa\n Влажность: {humidity} %")
                            weather_message_tomorrow.append(f"\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Ощущается как: {feels_like} ℃ \n Влажность: {humidity} %")
                return weather_message_tomorrow
        except Exception as e:
            print("Exception: ", e)
            with open("error.txt",'w',encoding='utf-8') as file:
                file.write(str(e))
            pass

    #gets data today forecast weather and return message
    elif (file_name=="today_forecast"):
        try:
            with open("data_forecast.json",'r',encoding='utf-8') as file:
                f = json.load(file)
                weather_message_today=[]
                isFirst = True
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
                        if isFirst:
                            #weather_message_today.append(f"\nПрогноз на сегодня ({date[0:10]})\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Максимальная температура: {cur_temp_max} ℃ \n Минимальная температура: {cur_temp_min} ℃ \n Ощущается как: {feels_like} ℃\n Давление: {humidity} hPa\n Влажность: {humidity} %")
                            weather_message_today.append(f"\nПрогноз на сегодня ({date[0:10]})\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Ощущается как: {feels_like} ℃\n Влажность: {humidity} %")
                            isFirst = False
                        else:
                            #weather_message_today.append(f"\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Максимальная температура: {cur_temp_max} ℃ \n Минимальная температура: {cur_temp_min} ℃ \n Ощущается как: {feels_like} ℃\n Давление: {humidity} hPa\n Влажность: {humidity} %")
                            weather_message_today.append(f"\nВремя: {date[11:16]}\n Описание: {weather_description} \n Температура: {cur_temp} ℃ \n Ощущается как: {feels_like} ℃ \n Влажность: {humidity} %")
                return weather_message_today
        except Exception as e:
            print("Exception: ", e)
            with open("error.txt",'w',encoding='utf-8') as file:
                file.write(str(e))
            pass
    #gets location and return it
    elif (file_name=="location"):
            try:
                with open("data_cur_weather.json",'r',encoding='utf-8') as file:
                        f = json.load(file)
                        location = f['name']
                return location
            except Exception as e:
                print("Exception: ", e)
                with open("error.txt",'w',encoding='utf-8') as file:
                    file.write(str(e))
                pass

#function to send message with todays forecast weather every morning
def sending_morning_mes(bot):
    get_forecast_weather()
    notif_users = []
    now = datetime.datetime.now()
    #check if message need to send tommorow
    hours = int(now.strftime("%H"))
    if (hours >= 9):
        tomorrow = datetime.date.today()+ datetime.timedelta(days=1)
        day = int(tomorrow.strftime("%d"))
    else:
        day = int(now.strftime("%d"))
    t_time = datetime.datetime(int(now.strftime("%Y")),int(now.strftime("%m")),day,13,3,0,)

    #some debug features
    print(f"\nMorning notification\n Time of Notification: {t_time}")
    print(f" Now: {now}")
    print(f" Time left: {(t_time -now).seconds}\n")

    time.sleep((t_time -now).seconds)

    #messaging
    while(True):
        get_forecast_weather()
        weather_message = "Доброе утро!)"
        weather_messages = get_from_file("today_forecast")
        for item in weather_messages:
            weather_message = weather_message + "\n" + item

        #get list of 'true' users
        with sqlite3.connect('users.sqlite') as conn:
            cur = conn.cursor()
            cur.execute("""SELECT *FROM Users WHERE notif = 1""")
            notif_users = cur.fetchall()

        #send them message
        for user in notif_users:
            #user[0] is id
            bot.send_message(user[0],weather_message)
            print(f"Morning notification for {user[3]}\n")
        time.sleep(86400)
    else:
        print("stopped")

#function to send message with tomorrow forecast weather every evening
def sending_evening_mes(bot):
    get_forecast_weather()
    notif_users = []
    now = datetime.datetime.now()
    #check if message need to send tomorrow
    hours = int(now.strftime("%H"))
    if (hours >= 21):
        tomorrow = datetime.date.today()+ datetime.timedelta(days=1)
        day = int(tomorrow.strftime("%d"))
    else:
        day = int(now.strftime("%d"))
    t_time = datetime.datetime(int(now.strftime("%Y")),int(now.strftime("%m")),day,21,0,0,)
    #some debug features
    print(f"\nEvening notification\n Time of Notification: {t_time}")
    print(f" Now: {now}")
    print(f" Time left: {(t_time -now).seconds}\n")
    time.sleep((t_time -now).seconds)
    while(True):
        get_forecast_weather()
        weather_message = "Добрый вечер!)"
        weather_messages = get_from_file("tomorrow_forecast")
        for item in weather_messages:
            weather_message = weather_message + "\n" + item

        #get list of 'true' users
        with sqlite3.connect('users.sqlite') as conn:
            cur = conn.cursor()
            cur.execute("""SELECT *FROM Users WHERE notif = 1""")
            notif_users = cur.fetchall()

        #send them message
        for user in notif_users:
            #user[0] is id
            bot.send_message(user[0],weather_message)
            print(f"Evening notification for {user[3]}\n")
        time.sleep(86400)
    else:
        print("stopped")

#FOR TESTS end
#MAIN
def main():
    #start time
    print(f'\nNum of active threads: {threading.activeCount()}')
    today = datetime.datetime.today()
    now = datetime.datetime.now()
    weekday_today = datetime.date.weekday(today)

    print(f"Prog started!\nMade by Gusarov2906\nTD :{today}\n")

    #start bot
    bot = bot_api.create_bot()

    #starts threads with notification
    th1 =Thread(target=sending_morning_mes, name="Thread1",args = (bot,), daemon = True)
    th2 =Thread(target=sending_evening_mes, name="Thread2",args = (bot,), daemon = True)
    th1.start()
    time.sleep(1)
    th2.start()
    time.sleep(1)
    print(f'\nNum of active threads: {threading.activeCount()}')

    #get location
    location = get_from_file("location")

    #settings for keyboard
    keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
    keyboard1.row('Погода сейчас','Прогноз погоды','Помощь')

    #bot.send_message(chat_id,chat_id)

    #starting message from bot
    @bot.message_handler(commands=['start'])
    def start_message(message):
        location = get_from_file("location")
        bot.send_message(message.chat.id, f'Привет, ты написал мне /start\nЭто бот мониторинга погоды\nВ данный момент локация погоды: {location}\nДля настроки уведолений зайдите в настройки /settings\nДля того чтобы зайти в меню помощи работает команда /help\n', reply_markup=keyboard1)
        #saving id to database if first open
        with sqlite3.connect('users.sqlite') as conn:
            cur = conn.cursor()
            chat_id = message.chat.id
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            username = message.from_user.username
            notif =1
            #print(chat_id,first_name,last_name,username)
            cur.execute('''INSERT OR IGNORE INTO Users (ID_chat,username,name,surname,notif)
                VALUES ( ?,?,?,?,? )''', ( chat_id,first_name,last_name,username,notif ) )
            conn.commit()

    #bot help menu
    @bot.message_handler(commands=['help'])
    def start_message(message):
        bot.send_message(message.chat.id, f'Помощь(доступные команды):\n/help\n/start\n/settings\n/start_notification\n/stop_notification\nПо техническим вопросам обращаться на:\ngusarov2906@gmail.com\n', reply_markup=keyboard1)

    #bot settings menu
    @bot.message_handler(commands=['settings'])
    def start_message(message):
        bot.send_message(message.chat.id, f'Настройки: \n /start_notification - вкл рассылку с утра и вечером\n /stop_notification - выкл рассылку с утра и вечером')


    #start notifications for all users
    @bot.message_handler(commands=['start_notification','stop_notification'])
    def send_text(message):
        with sqlite3.connect('users.sqlite') as conn:
            cur = conn.cursor()

            if (message.text=='/start_notification'):
                print("\nEnable notifications")
                cur.execute("""UPDATE Users SET notif = 1
                WHERE ID_chat = ?""", (message.chat.id,))
                bot.send_message(message.chat.id,f'\nУведомления включенны')

            elif(message.text=='/stop_notification'):
                print("\nDissable notifications")
                cur.execute("""UPDATE Users SET notif = 0
                WHERE ID_chat = (?)""",(message.chat.id,))
                bot.send_message(message.chat.id,f'\nУведомления выключенны')

            conn.commit()


    #menu from keyboard
    @bot.message_handler(content_types=['text'])
    def send_text(message):
        today = datetime.datetime.today()
        now = datetime.datetime.now()
        weekday_today = datetime.date.weekday(today)
        print(f"Got message: {message.text} ID: {message.chat.id} Time: {now}")


        if message.text == 'Погода сейчас':
            get_current_weather()
            weather_message =f'Сейчас: {now.strftime("%x")} {now.strftime("%X")}'
            tmp = get_from_file("now")
            weather_message += tmp
            bot.send_message(message.chat.id,weather_message)

        if message.text == 'Прогноз погоды':

            inline_keyboard_1 = types.InlineKeyboardMarkup(row_width = 3)
            item1 = types.InlineKeyboardButton("Сегодня", callback_data = "today")
            item2 = types.InlineKeyboardButton("Завтра", callback_data = "tommorow")
            item3 = types.InlineKeyboardButton("На 5 дней", callback_data = "week_forecast")
            inline_keyboard_1.add(item1,item2,item3)
            bot.send_message(message.chat.id,"На какой день вы хотите прогноз?",parse_mode='html', reply_markup=inline_keyboard_1)

        if message.text == 'Помощь':
            bot.send_message(message.chat.id, f'Помощь(доступные команды):\n/help\n/start\n/settings\n/start_notification\n/stop_notification\nПо техническим вопросам обращаться на:\ngusarov2906@gmail.com\n', reply_markup=keyboard1)

    @bot.callback_query_handler(func = lambda call:True)
    def callback_inline(call):
        try:
            if call.message:
                print(f"Got message: {call.data} ID:{call.message.chat.id} Time: {now}")
                if call.data == "today":
                    weather_messages = []
                    weather_message = ""
                    weather_messages = get_from_file("today_forecast")
                    for item in weather_messages:
                        weather_message = weather_message + "\n" + item
                    bot.send_message(call.message.chat.id,weather_message)
                elif call.data == "tommorow":
                    weather_messages = []
                    weather_message = ""
                    weather_messages = get_from_file("tomorrow_forecast")
                    for item in weather_messages:
                        weather_message = weather_message + "\n" + item
                    bot.send_message(call.message.chat.id,weather_message)
                elif call.data == "week_forecast":
                    weather_messages = []
                    weather_message = ""
                    weather_messages = get_from_file("week_forecast")
                    last_item = weather_messages[0]
                    for item in weather_messages:
                        weather_message = weather_message + "\n" + item
                        last_item = item
                    bot.send_message(call.message.chat.id,weather_message)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="На какой день вы хотите прогноз?",
                reply_markup=None)

        except Exception as e:
                with open("error.txt",'w',encoding='utf-8') as file:
                    file.write(str(e))
        """
            weather_messages = []
            weather_message = ""
            weather_messages = get_from_file("week_forecast")
            last_item = weather_messages[0]
            for item in weather_messages:
                weather_message = weather_message + "\n" + item
                last_item = item
            bot.send_message(message.chat.id,weather_message)

        if message.text == 'Погода сегодня':
            weather_messages = []
            weather_message = ""
            weather_messages = get_from_file("today_forecast")
            for item in weather_messages:
                weather_message = weather_message + "\n" + item
            bot.send_message(message.chat.id,weather_message)

        if message.text == 'Погода завтра':
            weather_messages = []
            weather_message = ""
            weather_messages = get_from_file("tomorrow_forecast")
            for item in weather_messages:
                weather_message = weather_message + "\n" + item
            bot.send_message(message.chat.id,weather_message)
        """
    #while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print("Exception: ", e)
        with open("error.txt",'w',encoding='utf-8') as file:
            file.write(str(e))
            time.sleep(5)


if __name__ == "__main__":
    main()
