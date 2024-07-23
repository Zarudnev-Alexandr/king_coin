import re

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.utils.keyboard import InlineKeyboardBuilder
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
    checked_inviter_id = check_args(inviter_id, message.from_user.id)
    print('👾👾🤖💩', checked_inviter_id)

    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=f'Играть {inviter_id}', web_app=types.WebAppInfo(url='https://king-coin.online:444/'))
    )

    await message.answer(
        "🌟 Добро пожаловать!",
        reply_markup=builder.as_markup()
    )


# @dp.message(CommandStart())
# async def command_start_process(message: Message, dialog_manager: DialogManager):
#     await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)
#
#
# start_dialog = Dialog(
#     Window(
#         Format('🌟 Добро пожаловать!'),
#         Group(
#             WebApp(Const('Играть'), Const('https://king-coin.online:444/'))
#         ),
#         state=StartSG.start
#     )
# )




# dp.include_router(start_dialog)
# setup_dialogs(dp)


async def on_startup(bot):
    print('бот полетел')


async def on_shutdown(bot):
    print('бот лег')


dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)

# dp.update.middleware(DataBaseSession(session_pool=session_maker))
dp.callback_query.middleware(CallbackAnswerMiddleware())

dp.run_polling(bot)