#>cd projects\pythonprojects\myweatherbot\myweatherbot\bot
#https://t.me/joinchat/AAAAAFfzbHvR_9TAg_DzPg
import json
import bot_api
import time
import telebot

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
            location = f['name']
            if (weather_status == "Clouds"):
                weather_status = "Облачно"
            weather_message = f"Статус погоды: {weather_status} \nТекущая температура: {cur_temp} ℃ \nМаксимальная температура: {cur_temp_max} ℃ \nМинимальная температура: {cur_temp_min} ℃ \nОщущается как: {feels_like} ℃"

    bot = bot_api.create_bot()

    keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
    keyboard1.row('Погода сейчас', 'Погода сегодня','Прогноз погоды')

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, f'Привет, ты написал мне /start\nЭто бот мониторинга погоды\nВ данный момент локация погоды: {location}', reply_markup=keyboard1)

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        if message.text == 'Погода сейчас':
                        bot.send_message(message.chat.id,weather_message)

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
