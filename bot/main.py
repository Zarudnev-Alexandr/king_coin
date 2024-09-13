import asyncio
import json
import re

import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager, StartMode, Dialog, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Group, WebApp
from aiogram_dialog.widgets.text import Format, Const
from environs import Env

from dialogs import start_dialog, enter_user_dialog, watch_daily_stat_dialog
from states import StartSG
from commands.quick_commands import check_args

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')
API_URL = env('API_URL')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


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
        InlineKeyboardButton(text=f'Play now👑', web_app=types.WebAppInfo(
            url=f'https://king-coin.online:444?ref={int(checked_inviter_id) if checked_inviter_id != "0" else None}'))
    )
    builder.row(
        InlineKeyboardButton(text='Subscribe to community', url='https://t.me/kingcoin_com'),
    )
    builder.row(
        InlineKeyboardButton(text='Our site', url='https://kingcoin.tech/')
    )

    await message.answer(
        """
        Hello, King!  
Your task is to become the biggest monkey in the crypto-jungles! 🌴  
Jump into the plane quickly and start collecting coins. Gather assets, analyze investment profitability, manage resources wisely, and earn the prestigious title of King Coin.  
Gather your crew by inviting new friends to the game—we will generously reward your participation during the listing.  
Also, don’t forget that KingCoin gives away 150 TON every week for activity in and outside the game.  
Good luck! The jungle is calling you!
        """,
        reply_markup=builder.as_markup()
    )


@dp.message(CommandStart())
async def command_start_no_referral(message: types.Message):

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Play now👑', web_app=types.WebAppInfo(url='https://king-coin.online:444/')),
    )
    builder.row(
        InlineKeyboardButton(text='Subscribe to community', url='https://t.me/kingcoin_com'),
    )
    builder.row(
        InlineKeyboardButton(text='Our site', url='https://kingcoin.tech/')
    )

    await message.answer(
        """
        Hello, King!  
Your task is to become the biggest monkey in the crypto-jungles! 🌴  
Jump into the plane quickly and start collecting coins. Gather assets, analyze investment profitability, manage resources wisely, and earn the prestigious title of King Coin.  
Gather your crew by inviting new friends to the game—we will generously reward your participation during the listing.  
Also, don’t forget that KingCoin gives away 150 TON every week for activity in and outside the game.  
Good luck! The jungle is calling you!
        """,
        reply_markup=builder.as_markup()
    )


@dp.message(Command('admin'))
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)

#
# async def command_daily(message: types.Message):
#     # URL вашего бэкенда
#     backend_url = "https://king-coin.online/api/users/daily_stats"
#
#     # Telegram ID пользователя, отправившего команду
#     tg_id = message.from_user.id
#
#     # Формируем запрос
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(backend_url, params={"tg_id": tg_id}) as response:
#                 if response.status == 404:
#                     await message.answer("Пользователь не найден.")
#                     return
#                 elif response.status == 403:
#                     await message.answer("У вас нет прав для использования этого API.")
#                     return
#                 elif response.status != 200:
#                     await message.answer("Произошла ошибка при запросе к серверу.")
#                     return
#
#                 # Получаем данные из ответа
#                 data = await response.json()
#
#                 # Формируем ответное сообщение для пользователя
#                 response_message = (
#                     f"📊 Статистика на сегодня:\n\n"
#                     f"👥 Количество пользователей: {data['count_of_all_users']}\n"
#                     # f"💰 Всего монет заработано: {data['all_earned_money']}\n"
#                     f"🆕 Пользователей зарегистрировано сегодня: {data['users_registered_today']}\n"
#                     f"📈 Пик онлайна сегодня: {data['online_peak']}"
#                 )
#                 await message.answer(response_message)
#
#     except Exception as e:
#         await message.answer(f"Произошла непредвиденная ошибка: {str(e)}")


# dp.include_router(start_dialog)


dp.include_router(start_dialog)
dp.include_router(enter_user_dialog)
dp.include_router(watch_daily_stat_dialog)
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