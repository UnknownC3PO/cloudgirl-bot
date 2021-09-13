import telebot
import config
from telebot import types
import data_b
import get_weather

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    sti = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, 'Hello! What city do you live in ?')


@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.chat.id, 'Commands:\nadd (city) - add or create new user.\ndel (city) - delete user.')


@bot.message_handler(content_types=['text'])
def change(message):
    if message.text[0:3].lower() == 'add':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton(f'{message.text[4:]}')
        markup.add(item)
        if data_b.get_user(message.chat.id, message.text[4:]):
            bot.send_message(message.chat.id, 'Added.', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'User already exists')
    elif message.text[0:3].lower() == 'del':
        bot.send_message(message.chat.id, data_b.del_user(message.chat.id, message.text[4:]))
    else:
        bot.send_message(message.chat.id, get_weather.get_weather_info(message.text))


if __name__ == '__main__':
    bot.polling(none_stop=True)
