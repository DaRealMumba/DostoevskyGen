"""
This is a echo bot.
It echoes any incoming text messages.
"""
import time
import numpy as np
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types

from gen_text import generate
import textwrap

START = """
Привет, %s!\nЯ генерирую текст в стиле Достоевского на основе его романов. Пришли мне слово или предложение, а я выдам тебе сгенерированный текст.
*Список команд*
/start - перезапуск
/info - расскажу о себе
/help - список доступных команд"""

HELP = """/start - перезапуск
/info - расскажу о себе
/help - список доступных команд"""

INFO = """Я обучен на 6 произведениях Достоевского: романы "Преступление и наказание", "Братья Карамазовы", "Бесы", "Идиот" и "Игрок" и повесть "Белые ночи"."""

INPUT_ERROR = """Запрос должен быть в текстовом виде.
Напомню, что /help выведет список доступных команд"""

load_dotenv()
API_TOKEN = os.getenv('TOKEN')

STICKER = 'CAACAgIAAxkBAAEDUdhhl6OoyyJjtOODeGjAcFYWJ9fWcAAC2gQAAgi3GQKtlIsa7N61vyIE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#     """
#     This handler will be called when user sends `/start` or `/help` command
#     """
#     await message.reply("Hi!\nI'm OXXXY_Bot!\nPowered by aiogram.")

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logging.info(f'{user_name} запустил бота в {time.asctime()}, его id = {user_id}')
    await message.reply(START % user_name, parse_mode='Markdown')

@dp.message_handler(commands=['info'])
async def process_info_command(message: types.Message):
    await message.reply(INFO)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(HELP)

# обработчик на случай, если был прислан не текст, а стикер, фото или любой другой тип данных
# @dp.message_handler(content_types='any')
# async def unknown_message(message: types.Message):
#     user_id = message.from_user.id
#     await bot.send_message(user_id, INPUT_ERROR)

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    user_id = message.from_user.id
    await bot.send_sticker(user_id, STICKER)
    mes = textwrap.fill(generate(message.text))
    await message.reply(mes)
    # await message.answer(textwrap.fill(generate(message.text), 50))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
