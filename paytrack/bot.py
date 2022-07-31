import datetime
import logging
import os
import asyncio as aio
import sqlite3
from aiogram import Bot, Dispatcher
import psycopg2
from aiogram.utils.markdown import hlink
API_TOKEN = os.environ.get("BOT_TOKEN")

# Configure logging
logging.basicConfig(format='Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s', level = logging.INFO, filename = '/var/log/bot.log', filemode = 'a')


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
loop = aio.get_event_loop()

async def thebot():
    logging.info(f'thebot def')

    """start polling in task"""
    loop.create_task(dp.start_polling())
    conn = psycopg2.connect(dbname=os.environ.get("SQL_DATABASE"), user=os.environ.get("SQL_USER"), 
                        password=os.environ.get("SQL_PASSWORD"), host=os.environ.get("SQL_HOST"))
    cursor = conn.cursor()
    
    now = datetime.datetime.now() + datetime.timedelta(hours=3)
    cursor.execute(f'select "Calendar_event".title, "Calendar_event".start, "Calendar_event".end, "Calendar_event".user_id, "Calendar_event".id, "Calendar_profile".telegram_id, "Calendar_calendar".telegrambool from public."Calendar_event" inner join public."Calendar_profile" ON ("Calendar_event".user_id = "Calendar_profile".user_id) inner join public."Calendar_calendar" ON ("Calendar_calendar".id = "Calendar_event".master_event_id) where "Calendar_event".end < \'{now}\' and "Calendar_event".paid = false and "Calendar_calendar".telegrambool = true;')
    data = cursor.fetchall()
    for i in data:
        try:
            await bot.send_message(int(i[5]), f"Как все прошло?\nЭто я про урок {str(i[1]).split(' ')[0]} у {i[0]} c {str(i[1]).split(' ')[1].split('+')[0]} до {str(i[2]).split(' ')[1].split('+')[0]}")
            await bot.send_message(int(i[5]),hlink('Ссылка на урок',f'https://tutorplan.ru/home/event/{i[4]}'),parse_mode='HTML',disable_web_page_preview=True)
        except:
            pass
        await aio.sleep(1)  
    await bot.send_message(687724238,f'Бот прошелся')
    await on_shutdown()

async def on_shutdown():
    dp.stop_polling()
    await dp.wait_closed()
    await bot.close()
    

def botstart():
    logging.info(f'bot start')
    loop.run_until_complete(thebot())
