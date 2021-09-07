import telebot
import requests
import time
import config
from telebot import types
import json

API = '1771722323:AAFcBrg-MdbkAHjMVZMfST89xhvoYEGSwTg'
bot = telebot.TeleBot(API)

user_data = {'users': []}

with open('db.json', 'w', encoding='utf-8') as db:
    json.dump(user_data, db, indent=4)


@bot.message_handler(commands=['start'])
def start(message):
    sti = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, 'Hello! What city do you live in ?')


@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.chat.id, 'Please, send me city name')


def parse(pogoda):
    cloud = pogoda['weather'][0]['description']
    city_name = pogoda['name']
    temp = 'Real temperature - ' + str(round((pogoda['main']['temp'] - 273.15), 2)) + '°C'
    feels_temp = 'Feels like - ' + str(round((pogoda['main']['feels_like'] - 273.15), 2)) + '°C'
    time_sunr = 'Sunrise - ' + time.ctime((pogoda['sys']['sunrise']))
    time_suns = 'Sunset - ' + time.ctime((pogoda['sys']['sunset']))
    info = city_name + '\n' + cloud.capitalize() + '\n' + feels_temp + '\n' + temp + '\n' + time_sunr + '\n' + time_suns
    return info


@bot.message_handler(func=lambda m: True)
def but_ton(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton(f'{message.text}')
    markup.add(item)
    with open('db.json', 'r', encoding='utf-8') as d:
        text_d = json.load(d)
        true_list = [True for i in text_d.get('users') if str(message.chat.id) in i]
        if True not in true_list:
            new_user = {}
            users = text_d.get('users')
            new_user[message.chat.id] = message.text
            users.append(new_user)
            user_data['users'] = users
            with open('db.json', 'w', encoding='utf-8') as db_w:
                json.dump(user_data, db_w, indent=4)
                del new_user
                try:
                    url = f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={config.API_key}'
                    r = requests.get(url)
                    if r.status_code == 200:
                        pogodka = r.json()
                        bot.send_message(message.chat.id, parse(pogodka), reply_markup=markup)
                    else:
                        bot.send_message(message.chat.id, 'Wrong city')
                except NameError:
                    bot.reply_to(message, 'Incorrect, try again')
        else:
            try:
                url = f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={config.API_key}'
                r = requests.get(url)
                if r.status_code == 200:
                    pogodka = r.json()
                    bot.reply_to(message, parse(pogodka))
                else:
                    bot.send_message(message.chat.id, 'Wrong city')
            except NameError:
                bot.reply_to(message, 'Incorrect, try again')
    user_data.clear()


if __name__ == '__main__':
    bot.polling(none_stop=True)
