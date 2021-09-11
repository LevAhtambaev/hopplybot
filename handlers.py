import pyowm

from main import bot, dp
from aiogram.types import Message
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = pyowm.OWM('e2f1f9ed06a58b710345e4818925b09b', config_dict)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    sti = 'CAACAgIAAxkBAAEC41phPPQMtzW82Coq2DQqDFW-g5VKGQACNwsAAq8H8Es5ef5tC1CiRCAE'
    await bot.send_sticker(message.chat.id, sti)
    await bot.send_message(message.chat.id, "Testing")
    me = message.from_user.first_name
    botname = await bot.get_me()
    # await bot.send_message(message.chat.id,
    #                       f"Добро пожаловать, {me}!\nЯ - {botname.frist_name}, укажи название города, в котором хочешь узнать погоду.")
    await bot.send_message(message.chat.id, f"Привет, {me}")
    await bot.send_message(message.chat.id, f"Привет, {botname.first_name}")


@dp.message_handler(content_types=['text'])
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
