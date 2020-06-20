import numpy as np
import random
import matplotlib.pyplot as plt

import sqlite3
import datetime
import time

import WeatherAPI
import MessageCreator


def write_cur_day_weather_to_db():

    now = datetime.datetime.now()
    hours = int(now.strftime("%H"))
    if (hours >= 15):
        tomorrow = datetime.date.today()+ datetime.timedelta(days=1)
        day = int(tomorrow.strftime("%d"))
    else:
        day = int(now.strftime("%d"))
    t_time = datetime.datetime(int(now.strftime("%Y")),int(now.strftime("%m")),day,13,44,10)

    #some debug features
    print(f"GraphCreator getter day temperature\n Time to first record: {t_time}")
    print(f" Now: {now}")
    print(f" Time left: {(t_time -now).seconds}\n")
    time.sleep((t_time -now).seconds)

    while(True):
        today = datetime.datetime.today()
        date = today.strftime("%d.%m.%Y")

        WeatherAPI.get_current_weather()
        Data = MessageCreator.get_data("cur_data")

        with sqlite3.connect('Database.sqlite') as conn:
            cur = conn.cursor()
            cur.execute('''INSERT OR IGNORE INTO Weather (Date)
            VALUES ( ?)''',(date,))
            cur.execute('''UPDATE Weather
             SET
                Day_temp = ?,
                Day_pressure = ?,
                Day_humidity = ?,
                Day_description = ?
             WHERE
                Date = ?''',(Data['cur_temp'],Data['pressure'],Data['humidity'],Data['description'],date))
            conn.commit()
            print(f"Record to database: {Data}")
            time.sleep(86400)
    else:
        print("stopped")




def write_cur_night_weather_to_db():

    now = datetime.datetime.now()
    hours = int(now.strftime("%H"))
    if (hours >= 3):
        tomorrow = datetime.date.today()+ datetime.timedelta(days=1)
        day = int(tomorrow.strftime("%d"))
    else:
        day = int(now.strftime("%d"))
    t_time = datetime.datetime(int(now.strftime("%Y")),int(now.strftime("%m")),day,13,44,15)

    #some debug features
    print(f"GraphCreator night temperature\n Time to first record: {t_time}")
    print(f" Now: {now}")
    print(f" Time left: {(t_time -now).seconds}\n")
    time.sleep((t_time -now).seconds)

    while(True):
        today = datetime.datetime.today()
        date = today.strftime("%d.%m.%Y")

        WeatherAPI.get_current_weather()
        Data = MessageCreator.get_data("cur_data")

        with sqlite3.connect('Database.sqlite') as conn:
            cur = conn.cursor()
            cur.execute('''INSERT OR IGNORE INTO Weather (Date)
            VALUES ( ?)''',(date,))
            cur.execute('''UPDATE Weather
             SET
              Night_temp = ?,
              Night_pressure = ?,
              Night_humidity = ?,
              Night_description = ?
            WHERE Date = ?''',(Data['cur_temp'],Data['pressure'],Data['humidity'],Data['description'],date))
            conn.commit()
            print(f"Record to database: Night_temp {Data}")
            time.sleep(86400)
    else:
        print("stopped")


def create_graph_image():
    x = np.linspace(-10, 10, 20)
    y = x**2
    plt.plot(x, y, color='red', marker='o', linestyle='--', markerfacecolor='blue')
    plt.plot(x, y, color='red', marker='o', linestyle='--', label='Линия 1')
    plt.plot(x, -y + 100, color='blue', marker='x', label='Линия 2')
    plt.grid() # сетка
    plt.legend(loc='best')

if __name__ == "__main__":
