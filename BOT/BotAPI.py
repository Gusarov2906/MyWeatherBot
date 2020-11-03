import telebot

def create_bot():
    bot = telebot.TeleBot('1200523410:AAHypg75ZIPuCJV8zsFHJgE4Dc4JAwGDE0s', threaded=False)
    #bot = telebot.TeleBot('1200523410:AAHypg75ZIPuCJV8zsFHJgE4Dc4JAwGDE0s')
    return bot
