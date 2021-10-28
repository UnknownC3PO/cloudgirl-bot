import telebot
import config
import os
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
