import telebot
import requests
import time
import config

bot = telebot.TeleBot(config.TOKEN)


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
def get_weather(message):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={config.API_key}'
        r = requests.get(url)
        if r.status_code == 200:
            pogodka = r.json()
            bot.reply_to(message, parse(pogodka))
        else:
            bot.reply_to(message, 'Incorrect, try again')
    except NameError:
        pass


bot.polling()
