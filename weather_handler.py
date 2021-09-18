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


@bot.message_handler(commands=['get'])
def get(message):
    bot.send_message(message.chat.id, data_b.get_user(message.chat.id))


@bot.message_handler(commands=['add'])
def add(message):
    if data_b.add_user(message.chat.id, message.text[5:]):
        bot.send_message(message.chat.id, 'Added.', reply_markup=buttons.city_button(message.text[5:]))


@bot.message_handler(commands=['update'])
def update(message):
    if data_b.update_user(message.chat.id, message.text[8:]):
        bot.send_message(message.chat.id, 'Updated.',
                         reply_markup=buttons.city_button(message.text[8:]))


@bot.message_handler(commands=['del'])
def delete(message):
    if data_b.del_user(message.chat.id, message.text[5:]):
        bot.send_message(message.chat.id, 'Deleted.')


@bot.message_handler(content_types=['text'])
def change(message):
    bot.send_message(message.chat.id, get_weather.get_weather_info(message.text))


if __name__ == '__main__':
    bot.polling(none_stop=True)
