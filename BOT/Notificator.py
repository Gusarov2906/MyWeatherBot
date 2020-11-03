import datetime
import time
import sqlite3

import WeatherAPI
import MessageCreator

#function to send message with todays forecast weather every morning
def sending_morning_mes(bot):
    WeatherAPI.get_forecast_weather()
    notif_users = []
    now = datetime.datetime.now()
    #check if message need to send tommorow
    hours = int(now.strftime("%H"))
    if (hours >= 9):
        tomorrow = datetime.date.today()+ datetime.timedelta(days=1)
        day = int(tomorrow.strftime("%d"))
    else:
        day = int(now.strftime("%d"))
    t_time = datetime.datetime(int(now.strftime("%Y")),int(now.strftime("%m")),day,9,0,0,)

    #some debug features
    print(f"Morning notification\n Time of Notification: {t_time}")
    print(f" Now: {now}")
    print(f" Time left: {(t_time -now).seconds}\n")

    time.sleep((t_time -now).seconds)
    ok = 0
    #messaging
    while(True):
        while(ok == 0):
            try:
                WeatherAPI.get_forecast_weather()
                weather_message = MessageCreator.create_message("morning notification")

                #get list of 'true' users
                with sqlite3.connect('Database.sqlite') as conn:
                    cur = conn.cursor()
                    cur.execute("""SELECT *FROM Users WHERE notif = 1""")
                    notif_users = cur.fetchall()

                #send them message
                print("\nMorning notification:")
                for user in notif_users:
                    #user[0] is id
                    bot.send_message(user[0],weather_message)
                    print(f" Morning notification for {user[1]}")
                print()
                ok =1
            except Exception:
                print("Exception in morning")
        ok = 0  
        time.sleep(86400)
    else:
        print("stopped")

#function to send message with tomorrow forecast weather every evening
def sending_evening_mes(bot):
    WeatherAPI.get_forecast_weather()
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
    print(f"Evening notification\n Time of Notification: {t_time}")
    print(f" Now: {now}")
    print(f" Time left: {(t_time -now).seconds}\n")
    time.sleep((t_time -now).seconds)
    ok = 0
    #messaging
    while(True):
        while(ok == 0):
            try:
                WeatherAPI.get_forecast_weather()
                weather_message = MessageCreator.create_message("evening notification")

                #get list of 'true' users
                with sqlite3.connect('Database.sqlite') as conn:
                    cur = conn.cursor()
                    cur.execute("""SELECT *FROM Users WHERE notif = 1""")
                    notif_users = cur.fetchall()

                #send them message
                print("\nEvening notification:")
                for user in notif_users:
                    #user[0] is id
                    bot.send_message(user[0],weather_message)
                    print(f" Evening notification for {user[1]}")
                print()
                ok = 1
            except Exception:
                print("Exception in evening")
        ok = 0        
        time.sleep(86400)
    else:
        print("stopped")
