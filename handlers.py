import telebot
import pyowm

from main import bot, dp
from aiogram.types import Message
from pyowm.utils.config import get_default_config
from telebot import types

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = pyowm.OWM('e2f1f9ed06a58b710345e4818925b09b', config_dict)


@bot.message_handler(commands=['vk'])
async def send_vk(message: Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_vk = types.InlineKeyboardButton(text='Лев Ахтамбаев', url='https://vk.com/hopply_time')
    markup.add(btn_vk)
    await bot.send_message(message.chat.id, "ВК автора :D", reply_markup=markup)


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    sti = 'CAACAgIAAxkBAAEC41phPPQMtzW82Coq2DQqDFW-g5VKGQACNwsAAq8H8Es5ef5tC1CiRCAE'
    await bot.send_sticker(message.chat.id, sti)
    await bot.send_message(message.chat.id,
                           "Добро пожаловать, {0.first_name}!\nЯ - {1.first_name}, укажи название города, в котором хочешь узнать погоду.".format(
                               message.from_user, bot.get_me()))


@bot.message_handler(content_types=['text'])
async def send_echo(message: Message):
    try:
        observation = owm.weather_manager().weather_at_place(message.text)
        w = observation.weather
        temperature = w.temperature('celsius')["temp"]
        status = w.detailed_status
        humidity = w.humidity
        wind = w.wind()['speed']
        answer = message.text + ": на улице " + str(round(temperature)) + " градусов. \n"
        answer += "В городе " + status + ". Влажность " + str(humidity) + "%. Скорость ветра " + str(wind) + " м/с."
        await bot.send_message(message.chat.id, answer)
    except:
        await bot.send_message(message.chat.id, "Город с таким названием не найден!")
