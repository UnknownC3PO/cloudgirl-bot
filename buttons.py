from telebot import types


def city_button(city):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton(f'{city}')
    markup.add(item)
    return markup
