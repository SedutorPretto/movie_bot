from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(dp: Dispatcher):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='film',
            description='Выбор фильма'
        ),
        BotCommand(
            command='cancel',
            description='Возврат к началу'
        )
    ]

    await dp.bot.set_my_commands(commands)