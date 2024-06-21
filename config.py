from aiogram import Bot, Dispatcher
from environs import Env

env = Env()
env.read_env('config.env')

BOT_TOKEN = env('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
