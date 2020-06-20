import datetime
import json

#CONSTANTS
days= ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

#fix week day(if it equals 7 it means that is first weekday, which equals 0)
def fix_wd(i):
    if (i==7):
        i=0
    return i
flag_to_end = False

#function to get data from files in current directory
def get_data(text):
    #gets date for current weather message
    if (text=="now"):
        try:
            with open("CurrentWeather.json",'r',encoding='utf-8') as file:
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

                    weather_message = f"\n Описание: {weather_description} \n Текущая температура: {cur_temp} ℃ \n Максимальная температура: {cur_temp_max} ℃ \n Минимальная температура: {cur_temp_min} ℃ \n Ощущается как: {feels_like} ℃\n Давление: {pressure} hPa\n Влажность: {humidity} %"
            return weather_message
        except Exception as e:
            print("!!Exception: ", e)
            with open("error.txt",'a',encoding='utf-8') as file:
                file.write("!!Exception: "+str(e))
            pass

    #gets data for 5 days forecast weather and return message
    elif (text=="week_forecast"):
        try:
            with open("ForecastWeather.json",'r',encoding='utf-8') as file:
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
                print("!!Exception: ", e)
                with open("error.txt",'a',encoding='utf-8') as file:
                    file.write("!!Exception: "+str(e))
                pass

    #gets data tomorrow forecast weather and return message
    elif (text=="tomorrow_forecast"):
        try:
            with open("ForecastWeather.json",'r',encoding='utf-8') as file:
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
            print("!!Exception: ", e)
            with open("error.txt",'a',encoding='utf-8') as file:
                file.write("!!Exception: "+str(e))
            pass

    #gets data today forecast weather and return message
    elif (text=="today_forecast"):
        try:
            with open("ForecastWeather.json",'r',encoding='utf-8') as file:
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
            print("!!Exception: ", e)
            with open("error.txt",'a',encoding='utf-8') as file:
                file.write("!!Exception: "+str(e))
            pass
    #gets location and return it
    elif (text=="location"):
            try:
                with open("CurrentWeather.json",'r',encoding='utf-8') as file:
                        f = json.load(file)
                        location = f['name']
                return location
            except Exception as e:
                print("!!Exception: ", e)
                with open("error.txt",'a',encoding='utf-8') as file:
                    file.write("!!Exception: "+str(e))
                pass
    #gets current data
    elif (text=="cur_data"):
                try:
                    with open("CurrentWeather.json",'r',encoding='utf-8') as file:
                            f = json.load(file)
                            data = dict(cur_temp = f['main']['temp'],
                                        pressure = f['main']['pressure'],
                                        humidity = f['main']['humidity'],
                                        description  = f['weather'][0]['description'])
                            return data
                except Exception as e:
                    print("!!Exception: ", e)
                    with open("error.txt",'a',encoding='utf-8') as file:
                        file.write("!!Exception: "+str(e))
                    pass


#function return ready to send message
def create_message(text):
    weather_messages = []
    weather_message = ""

    if (text=="now"):
        now = datetime.datetime.now()
        weather_message =f'Сейчас: {now.strftime("%x")} {now.strftime("%X")}'
        tmp = get_data(text)
        weather_message += tmp
        return weather_message

    elif (text=="today_forecast" or text=="tomorrow_forecast"):
        weather_messages = get_data(text)
        for item in weather_messages:
            weather_message = weather_message + "\n" + item
        return weather_message

    elif (text=="week_forecast"):
        weather_messages = get_data(text)
        last_item = weather_messages[0]
        for item in weather_messages:
            weather_message = weather_message + "\n" + item
            last_item = item
        return weather_message

    elif (text=="morning notification"):
        weather_message = "Доброе утро!)"
        weather_messages = get_data("today_forecast")
        for item in weather_messages:
            weather_message = weather_message + "\n" + item
        return weather_message

    elif (text=="evening notification"):
        weather_message = "Добрый вечер!)"
        weather_messages = get_data("tomorrow_forecast")
        for item in weather_messages:
            weather_message = weather_message + "\n" + item
        return weather_message
