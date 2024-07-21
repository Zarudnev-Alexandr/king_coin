from typing import Any

import requests
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, User, CallbackQuery
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import DialogManager, StartMode, setup_dialogs, Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Url, WebApp, Button, ScrollingGroup, Select, Back, Row, Next, Group
from aiogram_dialog.widgets.text import Const, Format
from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')
API_URL = env('API_URL')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


class StartSG(StatesGroup):
    start = State()


@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


start_dialog = Dialog(
    Window(
        Format('🌟 Добро пожаловать!'),
        Group(
            WebApp(Const('Играть'), Const('https://music.yandex.ru/home'))
        ),
        state=StartSG.start
    )
)




dp.include_router(start_dialog)
setup_dialogs(dp)


async def on_startup(bot):
    print('бот полетел')


async def on_shutdown(bot):
    print('бот лег')


dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)

# dp.update.middleware(DataBaseSession(session_pool=session_maker))
dp.callback_query.middleware(CallbackAnswerMiddleware())

dp.run_polling(bot)