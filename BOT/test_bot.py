import telebot

bot = telebot.TeleBot('1295322486:AAEMsiLCEpVH6AzKa9_mS6hN7CwLBLU4e9Y')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

bot.polling()
