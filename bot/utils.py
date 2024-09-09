from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from states import StartSG, EnterUserSG, WatchDailyStatSG


async def switch_to_main_menu(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.done()
    await dialog_manager.start(state=StartSG.start)


async def switch_to_add_user(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.done()
    await dialog_manager.start(state=EnterUserSG.enter_id)


async def switch_to_watch_daily_stat(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.done()
    await dialog_manager.start(state=WatchDailyStatSG.start)
