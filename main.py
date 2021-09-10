import telebot
import pyowm

from pyowm.utils.config import get_default_config
from telebot import types

bot = telebot.TeleBot("1951830803:AAHSTgjCwE0zXi018QU0gUNt0N6S2g6PJAE", parse_mode=None)

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = pyowm.OWM('e2f1f9ed06a58b710345e4818925b09b', config_dict)


@bot.message_handler(commands=['vk'])
def send_vk(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_vk = types.InlineKeyboardButton(text='Лев Ахтамбаев', url='https://vk.com/hopply_time')
    markup.add(btn_vk)
    bot.send_message(message.chat.id, "ВК автора :D", reply_markup=markup)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    sti = 'CAACAgIAAxkBAAEC3KxhNdjaRWshNWylS4A9NDwZo2IElAAClwUAAtJaiAGo2U4o023ROCAE'
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id,
                     "Добро добро пожаловать, {0.first_name}!\nЯ - {1.first_name}, укажи название города, в котором хочешь узнать погоду.".format(
                         message.from_user, bot.get_me()))

    #bot.reply_to(message, "Привет! Напиши название города, в котором хочешь узнать погоду.")


@bot.message_handler(content_types=['text'])
def send_echo(message):
    try:
        observation = owm.weather_manager().weather_at_place(message.text)
        w = observation.weather
        temperature = w.temperature('celsius')["temp"]
        status = w.detailed_status
        humidity = w.humidity
        wind = w.wind()['speed']
        answer = message.text + ": на улице " + str(round(temperature)) + " градусов. \n"
        answer += "В городе " + status + ". Влажность " + str(humidity) + "%. Скорость ветра " + str(wind) + " м/с."
        bot.send_message(message.chat.id, answer)
    except:
        bot.send_message(message.chat.id, "Город с таким названием не найден!")


bot.polling(none_stop=True)
