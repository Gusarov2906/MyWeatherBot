#>cd projects\pythonprojects\myweatherbot\myweatherbot\bot
#https://t.me/joinchat/AAAAAFfzbHvR_9TAg_DzPg
import json
import bot_api
import time

CHANNEL_NAME = '@gusarov2906_channel'

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
    bot = bot_api.create_bot()
    @bot.message_handler(commands=['start'])
    def start_message(message):
        while(True):
            bot.send_message(CHANNEL_NAME, 'Привет, ты написал мне /start')
            bot.send_message(CHANNEL_NAME, weather_status)
            time.sleep(60)

    print(weather_status)
    print(weather_description)
    print(cur_temp)
    print(cur_temp_min)
    print(cur_temp_max)
    print(feels_like)
    print(pressure)
    print(humidity)

    bot.polling()



#    with open("data_weather.txt",'r') as file:
#            f = file.read()
#            print(f)


except Exception as e:
    print("Exception: ", e)
    pass
