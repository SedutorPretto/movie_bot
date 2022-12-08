from aiogram.utils import executor
from create_bot import dp, bot
from utils.handlers import register_handlers
from utils.commands import set_commands

async def on_startup(dp):
    print('Bot is online!')
    await set_commands(dp)

register_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)