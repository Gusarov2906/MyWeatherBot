import telebot

def create_bot():
    bot = telebot.TeleBot('xxx', threaded=False)
    return bot
