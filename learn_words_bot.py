from aiogram import executor

import config
from handlers import client
from create_bot import dp, bot
from data_bases import sqlite_db


async def on_startup(_):
    print('Bot is running')
    sqlite_db.sql_start()

# async def on_startup(dp):
#     print('Бот запущено')
#     sqlite_db.sql_start()
#     await bot.set_webhook(config.URL_APP)
#
# async def on_shutdown(dp):


client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
