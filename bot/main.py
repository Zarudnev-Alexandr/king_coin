import asyncio
import json
import re

import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager, StartMode, Dialog, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Group, WebApp
from aiogram_dialog.widgets.text import Format, Const
from environs import Env

from commands.quick_commands import check_args

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')
API_URL = env('API_URL')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


class StartSG(StatesGroup):
    start = State()


@dp.message(CommandStart(
    deep_link=True,
    magic=F.args.regexp(re.compile(r'ref_(\d+)'))
))
async def command_start_process(message: types.Message,
                                command: CommandObject):
    inviter_id = command.args.split("_")[1] if command.args else ''
    checked_inviter_id = await check_args(inviter_id, message.from_user.id)

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=f'Играть сейчас! 👑', web_app=types.WebAppInfo(
            url=f'https://king-coin.online:444?ref={int(checked_inviter_id) if checked_inviter_id != "0" else None}'))
    )
    builder.row(
        InlineKeyboardButton(text='Подписаться на сообщество', url='https://t.me/kingcoin_com'),
    )
    builder.row(
        InlineKeyboardButton(text='Наш сайт', url='https://kingcoin.tech/')
    )

    await message.answer(
        """
        Привет, King!
Твоя задача - стать самой большой обезьяной в крипто-джунглях!🌴
Быстрее прыгай в самолёт и начинай собирать монеты. Собирай активы, анализируй прибыльность инвестиций, разумно распоряжайтесь ресурсами и получи престижный титул King Coin.
Собирай свою стаю, приглашая новых друзей в игру - мы щедро вознаградим твоё участие во время листинга.
А так же не забывай, что KingCoin каждую неделю раздает 150 TON за активность в игре и за её пределами.
Удачи! Джунгли тебя зовут! 
        """,
        reply_markup=builder.as_markup()
    )


@dp.message(CommandStart())
async def command_start_no_referral(message: types.Message):

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Играть сейчас! 👑', web_app=types.WebAppInfo(url='https://king-coin.online:444/')),
    )
    builder.row(
        InlineKeyboardButton(text='Подписаться на сообщество', url='https://t.me/kingcoin_com'),
    )
    builder.row(
        InlineKeyboardButton(text='Наш сайт', url='https://kingcoin.tech/')
    )

    await message.answer(
        """
        Привет, King!
Твоя задача - стать самой большой обезьяной в крипто-джунглях!🌴
Быстрее прыгай в самолёт и начинай собирать монеты. Собирай активы, анализируй прибыльность инвестиций, разумно распоряжайтесь ресурсами и получи престижный титул King Coin.
Собирай свою стаю, приглашая новых друзей в игру - мы щедро вознаградим твоё участие во время листинга.
А так же не забывай, что KingCoin каждую неделю раздает 150 TON за активность в игре и за её пределами.
Удачи! Джунгли тебя зовут! 
        """,
        reply_markup=builder.as_markup()
    )


# dp.include_router(start_dialog)
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