import sqlite3
from aiogram import types
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import CallbackQuery
import random
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import secrets
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

#token = '5484443497:AAGNv3JDqCFMDMt0SLEVZXBv39kH3GKeUPs'
token = '5136783035:AAFxDeRpBQhLBsKBHfg0DoYhgQIKeTarQzo'
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()




@dp.message_handler(commands=["start"])
async def start(message):
    connector = sqlite3.connect('users.db')
    cursor = connector.cursor()
    cursor.execute("SELECT count(*) FROM users where id = ? ", (message.from_user.id,))
    q = cursor.fetchone()
    if q[0] == 0 :
        cursor.execute(f"INSERT INTO USERS  VALUES(?,?)", (message.from_user.id,"0"))
        connector.commit()
        await bot.send_message(message.from_user.id, "Вам отправится сигнал, как только он появится")
    else:
        await bot.send_message(message.from_user.id, "Вам отправится сигнал, как только он появится")


@dp.message_handler(content_types=['text'])
async def command(message):
    if message.text == "lucky_bot_team":
        connector = sqlite3.connect('users.db')
        cursor = connector.cursor()
        cursor.execute("Update users set good = 1 where id = ?",(message.from_user.id,))
        connector.commit()
        await bot.send_message(message.from_user.id, "Код принят, в скором времени вы будете получать сигналы!")



@scheduler.scheduled_job('interval', seconds=5)
async def send_kef():
  try:
    connector = sqlite3.connect('users.db')
    cursor = connector.cursor()
    cursor.execute("SELECT id FROM users where good =1")
    users = cursor.fetchall()

    connector2 = sqlite3.connect('history.db')
    cursor2 = connector2.cursor()
    cursor2.execute("SELECT id,kef FROM history ORDER BY id DESC LIMIT 15")
    history = cursor2.fetchall()
    count = 0

    for i in range(15):
        if float(history[i][1]) < 10:
            count += 1
    if count == 15:
        for i in users:
          try:
            await bot.send_message(i[0],"❗❗❗В следующие 10 раундов будет 10x")
          except:
            1
        await func()
  except:
    1

async def func():
    connector2 = sqlite3.connect('history.db')
    cursor2 = connector2.cursor()
    cursor2.execute("SELECT id,kef FROM history ORDER BY id DESC LIMIT 15")
    history = cursor2.fetchall()
    connector = sqlite3.connect('users.db')
    cursor = connector.cursor()
    cursor.execute("SELECT id FROM users where good =1")
    users = cursor.fetchall()
    while 1 == 1:

        cursor2.execute("SELECT id,kef FROM history ORDER BY id DESC LIMIT 1")
        last = cursor2.fetchone()

        if last[0] == int(history[0][0]) + 10 and float(last[1]) < 10:
            for i in users:
              try:
                await bot.send_message(i[0], "❌10x не выпало")
              except:
                1
            break
        elif float(last[1]) >= 10:
            for i in users:
              try:
                await bot.send_message(i[0], f"✅10x выпало на {int(last[0]) - int(history[0][0])} раунде")
              except:
                1
            break
        else:
            continue


scheduler.start()
executor.start_polling(dp,skip_updates=True)
