from aiogram import types, Dispatcher
from movie_bot.bot.create_bot import dp, bot
from .keyboard import kb_client
from random import randint

import string, time, sqlite3

async def start(message: types.Message):
    await message.answer("Я простой бот и могу отправить тебе фильм.", reply_markup=kb_client)

async def movie(message: types.Message):
    await message.answer('Роюсь в архиве...')
    n = randint(1, 250)
    base = sqlite3.connect('C:\\Users\\User\\Desktop\\movie_bot\\movie_bot\\content\\kino_bot.db')
    cur = base.cursor()
    cur.execute(f'SELECT * FROM main WHERE number = {n}')
    res = cur.fetchone()
    caption = f"{res[2]} / {res[1]}\n\n " \
              f"Оценки: KP:{res[3]}, IMDb:{round(float(res[4]), 1)}\n\n" \
              f"Продолжительность: {res[5]}\n\n" \
              f"Год выхода: {res[6]}\n\n" \
              f"Жанры: {res[7]}\n\n" \
              f"Сюжет: {res[8]}" #TODO try namedtuple
    photo = types.InputFile(f'C:\\Users\\User\\Desktop\\movie_bot\\movie_bot\\content\\{res[1].replace(":", "-")}.jpg')
    time.sleep(1)
    await bot.send_photo(message.chat.id, photo, caption=caption)

async def cancel(message: types.Message):
    await message.answer("Ah shit, here we go again...")


async def all_mess(message: types.Message):
    if 'фильм' in message.text.lower():
        await movie(message)
    with open('utils/cenzorship.txt', encoding='utf-8') as file:
        cenzorship = [i.strip() for i in file.readlines()]
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(cenzorship)):
        await message.answer('Обратитесь к <b>психологу</b>\n Место для рекламы', parse_mode='HTML')
        await message.delete()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(movie, commands=['film'])
    dp.register_message_handler(cancel, commands=['cancel'])
    dp.register_message_handler(all_mess)