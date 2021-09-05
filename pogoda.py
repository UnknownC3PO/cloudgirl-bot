import telebot
import requests
import time
import config
from telebot import types
import os
from flask import Flask, request
import logging

bot = telebot.TeleBot(config.TOKEN)

user_data = {}

server = Flask(__name__)

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
    user_data[message.from_user.id] = f'{message.text}'
    with open('user_data.txt', 'r') as db:
        if str(message.from_user.id) not in db.read():
            with open('user_data.txt', 'a') as db_r:
                db_r.write(f'{user_data}\n')
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


@server.route('/' + config.TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your_heroku_project.com/' + config.TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

