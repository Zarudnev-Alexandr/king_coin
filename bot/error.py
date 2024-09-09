from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button

from states import StartSG


async def error_id(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    await message.answer(
        text='Вы ввели неверный id. Попробуйте еще раз'
    )


async def close_dialog(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.done()
    await dialog_manager.start(state=StartSG.start)


async def no_text(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    await message.answer(text='Вы ввели вообще не текст!')


async def error_first_name(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректное название. Попробуйте еще раз'
    )


