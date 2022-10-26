import os

from aiogram import executor

import config
from handlers import client
from create_bot import dp, bot
from data_bases import sqlite_db


# async def on_startup(_):
#     print('Бот запущено')
#     sqlite_db.sql_start()

async def on_startup(dp):
    print('Бот запущено')
    sqlite_db.sql_start()
    await bot.set_webhook(config.URL_APP)


async def on_shutdown(dp):
    await bot.delete_webhook()


client.register_handlers_client(dp)

# executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
executor.start_webhook(
    dispatcher=dp,
    webhook_path='',
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host='0.0.0.0',
    port=int(os.environ.get("PORT", 5000))
)
