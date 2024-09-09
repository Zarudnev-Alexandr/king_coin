from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from states import EnterUserSG


async def correct_id(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:

    dialog_manager.dialog_data['id'] = text

    await dialog_manager.next()


async def correct_first_name(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data['first_name'] = text
    await dialog_manager.next()


async def skip_input_first_name(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['first_name'] = ''
    await dialog_manager.next()


async def correct_last_name(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data['last_name'] = text
    await dialog_manager.next()


async def skip_input_last_name(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['last_name'] = ''
    await dialog_manager.next()


async def correct_username(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data['username'] = text
    await dialog_manager.next()


async def skip_input_username(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['username'] = ''
    await dialog_manager.next()

