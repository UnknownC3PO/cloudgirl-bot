from bot import bot
import config
import data_b
import get_weather
import buttons


@bot.message_handler(commands=['start'])
def start(message):
    sti = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, 'Hello! What city do you live in ?')


@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.chat.id,
                     '''Commands:\nget - for get info about user.\nadd (your city) - add\
 or create new user.\ndel (your city) - delete user.\nupdate (your city) - update user.''')


@bot.message_handler(content_types=['text'])
def change(message):
    if message.text.lower() == 'get':
        bot.send_message(message.chat.id, data_b.get_user(message.chat.id))
    elif message.text[0:3].lower() == 'add':
        if data_b.add_user(message.chat.id, message.text[4:]):
            bot.send_message(message.chat.id, 'Added.', reply_markup=buttons.city_button(message.text[4:]))
        else:
            bot.send_message(message.chat.id, 'User already exists')
    elif message.text[0:6].lower() == 'update':
        bot.send_message(message.chat.id, data_b.update_user(message.chat.id, message.text[7:]),
                         reply_markup=buttons.city_button(message.text[7:]))
    elif message.text[0:3].lower() == 'del':
        bot.send_message(message.chat.id, data_b.del_user(message.chat.id, message.text[4:]))
    else:
        bot.send_message(message.chat.id, get_weather.get_weather_info(message.text))


if __name__ == '__main__':
    bot.polling(none_stop=True)
