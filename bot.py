import json
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyaterochka_parser_js import all_cat_str, cat_id, subcats, items
from magnit_parser_js import magnit_main
from fasol_parser import fasol_main
import datetime
import logging

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher(bot)



logging.basicConfig(level=logging.INFO)
# logging.info("вывод в консоль")

current_date = datetime.datetime.now().strftime('%m-%d')

first_text = '''
Здравствуйте! 
Этот бот поможет вам узнать все скидки и акции
в популярных торговых точках города Санкт-Петербург. 
'''



@dp.message_handler(commands = "start")
async def start_command(message: types.Message, ):
    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="Магнит")
    button_2 = types.KeyboardButton(text="Пятерочка")
    button_3 = types.KeyboardButton(text="Фасоль")
    keyboard.add(button_1, button_2, button_3)
    await message.reply(text=first_text, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text.lower() == "магнит")
async def magnit_parser(message: types.Message, ):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'В данный момент не работает!')
    # name = await magnit_main()
    # with open(name, 'rb') as file:
    #     await message.answer_document(file)
    # os.remove(name)


@dp.message_handler(lambda message: message.text.lower() == "пятерочка")
async def pyaterochka_parser(message: types.Message, ):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Используйте команду /categories для получения категорий.')



@dp.message_handler(commands=['categories'])
async def cmd_categories(message: types.Message):
    file = await all_cat_str()
    categories = json.loads(cat_id(file))  # Декодируем JSON в Python объект
    keyboard = InlineKeyboardMarkup(row_width=2)  # Максимум 2 кнопки в строке

    # Создаем кнопки для каждой категории
    for cat in categories:
        button = InlineKeyboardButton(cat['name'], callback_data=f"cat_{cat['id']}")
        keyboard.add(button)

    await message.answer("Выберите категорию:", reply_markup=keyboard)


# Обработка выбора категории
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('cat_'))
async def process_category(callback_query: types.CallbackQuery):
    cat_id = callback_query.data.split('_')[1]
    file = await all_cat_str()
    subcategories = json.loads(subcats(file, cat_id))  # Декодируем подкатегории
    keyboard = InlineKeyboardMarkup(row_width=2)

    # Создаем кнопки для каждой подкатегории
    for sub in subcategories:
        button = InlineKeyboardButton(sub['name'], callback_data=f"subcat_{sub['id']}")
        keyboard.add(button)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Выберите подкатегорию:", reply_markup=keyboard)


# Обработка выбора подкатегории
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('subcat_'))
async def process_subcategory(callback_query: types.CallbackQuery):
    subcat_id = callback_query.data.split('_')[1]
    items_list, foto_url = await items(subcat_id)  # Получаем товары для выбранной подкатегории
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Товары:")
    for foto, item in enumerate(items_list):
        print(foto)
        await bot.send_photo(callback_query.from_user.id, foto_url[foto][0])
        await bot.send_message(callback_query.from_user.id, item)


@dp.message_handler(lambda message: message.text.lower() == "фасоль")
async def fasol_parser(message: types.Message, ):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Подождите...')
    name = await fasol_main()
    with open(name, 'rb') as file:
        await message.answer_document(file)
    os.remove(name)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
