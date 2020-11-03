import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sqlite3
import datetime
import time
import os
import threading

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
    t_time = datetime.datetime(int(now.strftime("%Y")),int(now.strftime("%m")),day,15,0,10)

    #some debug features
    print(f"GraphCreator day temperature\n Time to first record: {t_time}")
    print(f" Now: {now}")
    print(f" Time left: {(t_time -now).seconds}\n")
    time.sleep((t_time -now).seconds)

    while(True):
        start_time = datetime.datetime.now()
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
            print(f"Record to database: Day temp {Data}")
            finish_time = datetime.datetime.now()
            time.sleep(86400-(finish_time-start_time).seconds)
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
    t_time = datetime.datetime(int(now.strftime("%Y")),int(now.strftime("%m")),day,3,0,10)

    #some debug features
    print(f"GraphCreator night temperature\n Time to first record: {t_time}")
    print(f" Now: {now}")
    print(f" Time left: {(t_time -now).seconds}\n")
    time.sleep((t_time -now).seconds)

    while(True):
        start_time = datetime.datetime.now()
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
            finish_time = datetime.datetime.now()
            time.sleep(86400-(finish_time-start_time).seconds)
    else:
        print("stopped")

def write_hourly_temperature_to_db():

        now = datetime.datetime.now()
        hours = int(now.strftime("%H"))
        minutes = int(now.strftime("%M"))
        if (hours+1<=23):
            day = int(now.strftime("%d"))
            t_time = datetime.datetime(int(now.strftime("%Y")),int(now.strftime("%m")),day,hours+1,0,10)
        else:
            tomorrow = datetime.date.today()+ datetime.timedelta(days=1)
            day = int(tomorrow.strftime("%d"))
            t_time = datetime.datetime(int(now.strftime("%Y")),int(now.strftime("%m")),day,0,0,10)
        #some debug features
        print(f"GraphCreator hourly temperature\n Time to first record: {t_time}")
        print(f" Now: {now}")
        print(f" Time left: {(t_time -now).seconds}\n")
        time.sleep((t_time -now).seconds)

        while(True):
            start_time = datetime.datetime.now()
            print(f'Num of active threads and procceses: {threading.activeCount()}')
            today = datetime.datetime.today()
            date = today.strftime("%d.%m.%Y")
            now = datetime.datetime.now()
            hours = int(now.strftime("%H"))
            minutes = int(now.strftime("%M"))
            cur_time = f'{hours}:{minutes}'

            WeatherAPI.get_current_weather()
            cur_temperature = MessageCreator.get_data("cur_temperature")

            with sqlite3.connect('Database.sqlite') as conn:
                cur = conn.cursor()
                cur.execute('''INSERT OR IGNORE INTO Temperature (Date,Time,Value)
                VALUES ( ?,?,?)''',(date,cur_time,cur_temperature))
                conn.commit()
                finish_time = datetime.datetime.now()
                time.sleep(3600-(finish_time-start_time).seconds)
        else:
            print("stopped")



#get data from database
def get_data_from_db(text):
    if (text=="Day_temp"):
        with sqlite3.connect('Database.sqlite') as conn:
            cur = conn.cursor()
            cur.execute('''SELECT Day_temp FROM Weather ORDER BY Date DESC LIMIT 10''')
            Day_temp = cur.fetchall()
            array_day_temp = []
            for i in range(len(Day_temp)):
                array_day_temp.append(Day_temp[i][0])
            print(array_day_temp)
            return array_day_temp
    elif (text=="Night_temp"):
        with sqlite3.connect('Database.sqlite') as conn:
            cur = conn.cursor()
            cur.execute('''SELECT Night_temp FROM Weather ORDER BY Date DESC LIMIT 10''')
            Night_temp = cur.fetchall()
            array_night_temp = []
            for i in range(len(Night_temp)):
                array_night_temp.append(Night_temp[i][0])
            print(array_night_temp)
            return array_night_temp
    elif (text=="Dates"):
        with sqlite3.connect('Database.sqlite') as conn:
            cur = conn.cursor()
            cur.execute('''SELECT Date FROM Weather ORDER BY Date DESC LIMIT 10''')
            Dates = cur.fetchall()
            array_dates = []
            for i in range(len(Dates)):
                array_dates.append(Dates[i][0][:5])
            print(array_dates)
            return array_dates
    elif (text=="cur_temperature"):
        with sqlite3.connect('Database.sqlite') as conn:
            cur = conn.cursor()
            cur.execute('''SELECT Date FROM Temperature ORDER BY Date DESC LIMIT 10''')
            Dates = cur.fetchall()
            array_dates = []
            for i in range(len(Dates)):
                array_dates.append(Dates[i][0][:5])
            print(array_dates)
            return array_dates

#func to rename files to make history circle
def history_image_renamer(i):
    index = i+1
    if ('history_'+f'{i}'+'.png' in os.listdir()):
        history_image_renamer(index)
        if(i!=5):
            os.replace('history_'+f'{i}'+'.png','history_'+f'{index}'+'.png')


def create_10days_graph_image(array_x,array_y1,array_y2):
    #x = np.arange(array_y.size)
    #y = np.array(array_y)
    #plt.figure()
    #plt.plot(np.array(array_x), y, color='red', marker='o', linestyle='--', markerfacecolor='blue')
    #plt.grid()
    #plt.legend(loc='best')
    #plt.show()

    array_x.reverse()
    array_y1.reverse()
    array_y2.reverse()
    fig, graph = plt.subplots()
    y1 = np.array(array_y1)
    y2 = np.array(array_y2)
    x = np.arange(y1.size)
    print(x)
    print(y1)
    print(y2)
    plt.plot(x, y1, color='#FF4500', marker='o', markerfacecolor='#FF4500',
                    linewidth=3, markersize=6, label='Дневная температура')
    plt.plot(x, y2, color='#000080', marker='o', markerfacecolor='#000080',
                    linewidth=3, markersize=6, label='Ночная температура')
    plt.grid()

    graph.minorticks_on()
    graph.grid(which='major',
        color = '#808080',
        linestyle = '--')

    graph.grid(which='minor',
        color = '#C0C0C0',
        linestyle = ':')

    graph.axis([0,9,min(y2)-5,max(y1)+5])

    graph.xaxis.set_major_locator(plt.MultipleLocator(1))
    graph.xaxis.set_minor_locator(plt.MultipleLocator(1))
    graph.yaxis.set_major_locator(plt.MultipleLocator(2))
    graph.yaxis.set_minor_locator(plt.MultipleLocator(0.5))

    graph.tick_params(
               axis = 'x',
               which = 'major',
               direction = 'inout',
               length = 10,
               width = 2,
               color = 'black',
               pad = 12,
               labelsize = 12,
               labelcolor = 'white',
               bottom = True,
               labelbottom = True)

    graph.tick_params(
               axis = 'y',
               which = 'major',
               direction = 'inout',
               length = 10,
               width = 2,
               color = 'black',
               pad = 3,
               labelsize = 12,
               labelcolor = 'white',
               left = True,
               labelleft = True)
               #labelrotation = 90)

    graph.tick_params(
               which = 'minor',
               direction = 'in',
               length = 5,
               width = 1,
               color='black',
               pad = 5,
               bottom = True,
               left = True)

    graph.set_xticks(x)
    graph.set_xticklabels(array_x)

    #graph.xaxis.set_major_locator(ticker.MultipleLocator(1))
    #graph.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    #graph.yaxis.set_major_locator(ticker.MultipleLocator(5))
    #graph.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    #xticks(range(9),array_x)
    graph.fill_between(x,y1,y2,facecolor='#00FF00',label='Диапазон температур')

    plt.xlabel('Дата', fontsize = 13, fontstyle = "italic", weight ='bold', color='white')
    plt.ylabel('Температура', fontsize = 13, fontstyle = "italic",weight='bold', color='white')
    plt.title('График температуры за последние 10 дней', fontsize = 15, weight='bold', color='white')

    legend = graph.legend(shadow = False)
    legend.get_frame().set_facecolor('#F0F8FF')

    graph.set_facecolor('#F0FFFF')
    fig.patch.set_facecolor('#483D8B')
    plt.text(0.3,33,"MyWeatherBot",fontsize = 16,color='#483D8B',weight ='bold')
    plt.text(8.05,10.5,"@gusarov2906",fontsize = 8.6,color='#483D8B')
    fig.set_figwidth(10)
    fig.set_figheight(8)

    plt.tight_layout()

    os.chdir(os.getcwd()+'/Graphs')
    if not('10days.png' in os.listdir()):
        plt.savefig(r'10days.png',quality=100,dpi=300,facecolor=fig.get_facecolor())
    else:
        history_image_renamer(1)
        os.rename('10days.png','history_1.png')
        plt.savefig(r'10days.png',quality=100,dpi=300,facecolor=fig.get_facecolor())

    plt.show()

def main():
    write_hourly_temperature_to_db()
    Day_temp = get_data_from_db("Day_temp")
    Night_temp = get_data_from_db("Night_temp")
    Dates = get_data_from_db("Dates")
    #create_10days_graph_image(Dates,Day_temp,Night_temp)

if __name__ == "__main__":
    main()
