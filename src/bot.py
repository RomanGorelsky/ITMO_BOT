import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types

from parser import get_curriculum_file

api = ""
with open("src/api.txt", "r") as myfile:
    for text in myfile:
        api += text

bot = AsyncTeleBot(api)

@bot.message_handler(commands=['help', 'start'])
async def url(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Искусственный Интеллект')
    markup.add(btn1)
    btn2 = types.KeyboardButton('Управление ИИ-продуктами/AI Product')
    markup.add(btn2)
    await bot.send_message(message.from_user.id, "Узнать об учебном плане программы:", reply_markup = markup)

@bot.message_handler(func=lambda message: True)
async def get_text_messages(message):

    if message.text == 'Искусственный Интеллект':
        await bot.send_message(message.from_user.id, 'Вот учебный план по программе "Искусственный Интеллект"')
        file_path = get_curriculum_file('Искусственный Интеллект')
        with open(file_path, 'rb') as doc:
            await bot.send_document(message.from_user.id, doc)

    elif message.text == 'Управление ИИ-продуктами/AI Product':
        await bot.send_message(message.from_user.id, 'Вот учебный план по программе "Управление ИИ-продуктами/AI Product"')
        file_path = get_curriculum_file('Управление ИИ-продуктами/AI Product')
        with open(file_path, 'rb') as doc:
            await bot.send_document(message.from_user.id, doc)
    
    else:
        await bot.send_message(message.from_user.id, 'Пожалуйста, выберите одну из программ')

asyncio.run(bot.polling(none_stop=True, interval=0)) #обязательная для работы бота часть