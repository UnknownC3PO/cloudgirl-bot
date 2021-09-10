import telebot
import config
from telebot import types
from data_b import *
from get_weather import *

bot = telebot.TeleBot(config.TOKEN)
del_u = ['Del', 'del', 'DEL']
add_u = ['Add', 'add', 'ADD']


@bot.message_handler(commands=['start'])
def start(message):
    sti = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, 'Hello! What city do you live in ?')


@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.chat.id, 'Commands:\nadd (city) - add or create new user.\ndel (city) - delete user.')


@bot.message_handler(content_types=['text'])
def add_del(message):
    if message.text[0:3] in add_u:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton(f'{message.text[4:]}')
        markup.add(item)
        if create_user(message.chat.id, message.text[4:]) == 'User already exists.':
            bot.send_message(message.chat.id, 'User already exists.')
        else:
            bot.send_message(message.chat.id, 'Added.', reply_markup=markup)
    elif message.text[0:3] in del_u:
        bot.send_message(message.chat.id, del_user(message.chat.id, message.text[4:]))
    else:
        bot.send_message(message.chat.id, get_weather_info(message.text))


if __name__ == '__main__':
    bot.polling(none_stop=True)
