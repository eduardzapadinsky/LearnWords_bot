import os
from aiogram import Bot, Dispatcher
import config


# bot = Bot(token=config.TOKEN)
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
