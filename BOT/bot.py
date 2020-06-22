#>cd projects\pythonprojects\myweatherbot\myweatherbot\bot
#@gusarov2906_weather_bot

#IMPORTS
import datetime
import time
import telebot
from telebot import types
import threading
from threading import Thread
import sqlite3
import sys

#import my modules
import BotAPI
import MessageCreator
import WeatherAPI
import Notificator
import GraphCreator

#MAIN
def main():
    #start time
    today = datetime.datetime.today()
    now = datetime.datetime.now()
    weekday_today = datetime.date.weekday(today)

    print(f'''\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
    Prog started!\nMade by Gusarov2906\nTD :{today}\n\n''')
    print(f'Num of active threads and procceses: {threading.activeCount()}')

    #start bot
    bot = BotAPI.create_bot()

    #starts threads with notification

    th1 =Thread(target=Notificator.sending_morning_mes, name="Thread1",args = (bot,))
    th2 =Thread(target=Notificator.sending_evening_mes, name="Thread2",args = (bot,))
    th3 =Thread(target=GraphCreator.write_cur_day_weather_to_db, name="Thread3")
    th4 =Thread(target=GraphCreator.write_cur_night_weather_to_db, name="Thread4")
    th5 =Thread(target=GraphCreator.write_hourly_temperature_to_db, name="Thread5")

    th1.start()
    time.sleep(2)
    th2.start()
    time.sleep(2)
    th3.start()
    time.sleep(2)
    th4.start()
    time.sleep(2)
    th5.start()
    time.sleep(2)
    print(f'Num of active threads: {threading.activeCount()}\n\n')

    #get location
    location = MessageCreator.get_data("location")


    #settings for keyboard
    keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
    keyboard1.row('Погода сейчас','Прогноз погоды','Помощь')

    #starting message from bot
    @bot.message_handler(commands=['start'])
    def start_message(message):

        now = datetime.datetime.now()
        print(f"Got message: start ID:{message.chat.id} Time: {now}")
        print()

        bot.send_message(message.chat.id, f'Привет, ты написал мне /start\nЭто бот мониторинга погоды\nВ данный момент локация погоды: {location}\nДля настроки уведолений зайдите в настройки /settings\nДля того чтобы зайти в меню помощи работает команда /help\n', reply_markup=keyboard1)
        #saving id to database if first open
        with sqlite3.connect('Database.sqlite') as conn:
            cur = conn.cursor()
            chat_id = message.chat.id
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            username = message.from_user.username
            notif =1
            #print(chat_id,first_name,last_name,username)
            cur.execute('''INSERT OR IGNORE INTO Users (ID_chat,username,name,surname,notif)
                VALUES ( ?,?,?,?,? )''', ( chat_id,username,first_name,last_name,notif ) )
            conn.commit()

    #bot help menu
    @bot.message_handler(commands=['help'])
    def start_message(message):

        now = datetime.datetime.now()
        print(f"Got message: help ID:{message.chat.id} Time: {now}")
        print()

        bot.send_message(message.chat.id, f'Помощь(доступные команды):\n/help\n/start\n/settings\n/start_notification\n/stop_notification\nПо техническим вопросам обращаться на:\ngusarov2906@gmail.com\n', reply_markup=keyboard1)

    #bot settings menu
    @bot.message_handler(commands=['settings'])
    def start_message(message):

        now = datetime.datetime.now()
        print(f"Got message: settings ID:{message.chat.id} Time: {now}")
        print()

        bot.send_message(message.chat.id, f'Настройки: \n /start_notification - вкл рассылку с утра и вечером\n /stop_notification - выкл рассылку с утра и вечером')


    #start notifications for all users
    @bot.message_handler(commands=['start_notification','stop_notification'])
    def send_text(message):

        now = datetime.datetime.now()
        print(f"Got message: start/stop notif ID:{message.chat.id} Time: {now}")

        with sqlite3.connect('Database.sqlite') as conn:
            cur = conn.cursor()

            if (message.text=='/start_notification'):
                print("Enable notifications\n")
                cur.execute("""UPDATE Users SET notif = 1
                WHERE ID_chat = ?""", (message.chat.id,))
                bot.send_message(message.chat.id,f'\nУведомления включенны')

            elif(message.text=='/stop_notification'):
                print("Dissable notifications\n")
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
            WeatherAPI.get_current_weather()
            weather_message = MessageCreator.create_message("now")
            bot.send_message(message.chat.id,weather_message)
            print()

        elif message.text == 'Прогноз погоды':

            inline_keyboard_1 = types.InlineKeyboardMarkup(row_width = 3)
            item1 = types.InlineKeyboardButton("Сегодня", callback_data = "today_forecast")
            item2 = types.InlineKeyboardButton("Завтра", callback_data = "tomorrow_forecast")
            item3 = types.InlineKeyboardButton("На 5 дней", callback_data = "week_forecast")
            inline_keyboard_1.add(item1,item2,item3)
            bot.send_message(message.chat.id,"На какой день вы хотите прогноз?",parse_mode='html', reply_markup=inline_keyboard_1)

        elif message.text == 'Помощь':
            bot.send_message(message.chat.id, f'Помощь(доступные команды):\n/help\n/start\n/settings\n/start_notification\n/stop_notification\nПо техническим вопросам обращаться на:\ngusarov2906@gmail.com\n', reply_markup=keyboard1)
            print()
        else:
            bot.send_message(message.chat.id, f'Проверьте правильность введенной команды.\n Для это можно воспользоваться /help', reply_markup=keyboard1)
            print()

    #inline keyboard handler
    @bot.callback_query_handler(func = lambda call:True)
    def callback_inline(call):
        try:
            if call.message:
                print(f"Got message: {call.data} ID:{call.message.chat.id} Time: {now}")

                if call.data == "today_forecast":
                    weather_message = MessageCreator.create_message(call.data)
                    bot.send_message(call.message.chat.id,weather_message)

                elif call.data == "tomorrow_forecast":
                    weather_message = MessageCreator.create_message(call.data)
                    bot.send_message(call.message.chat.id,weather_message)

                elif call.data == "week_forecast":
                    weather_message = MessageCreator.create_message(call.data)
                    bot.send_message(call.message.chat.id,weather_message)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="На какой день вы хотите прогноз?",
                reply_markup=None)
                print()
        except Exception as e:
                with open("error.txt",'a',encoding='utf-8') as file:
                    file.write("!Exception: "+str(e))

    #bot pulling cycle
    while True:
        try:
            bot.infinity_polling(True)
        except KeyboardInterrupt:
                print ('Interrupted')
                sys.exit(0)
        except Exception as e:
            print("!Exception: ", e)
            with open("error.txt",'a',encoding='utf-8') as file:
                file.write("!Exception: "+str(e))
                time.sleep(20)



#start main
if __name__ == "__main__":
    main()
