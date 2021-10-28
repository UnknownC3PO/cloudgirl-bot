import telebot
#import config
TOKEN = None
with open("token.txt") as f:
    TOKEN = f.read().strip()
bot = telebot.TeleBot(TOKEN)
