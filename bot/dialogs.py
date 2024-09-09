from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, Back, Next
from aiogram_dialog.widgets.text import Const, Format

from check import id_check, descr_check
from correct import correct_id, correct_first_name, skip_input_first_name, correct_last_name, skip_input_last_name, \
    correct_username, skip_input_username
from error import error_id, no_text, close_dialog, error_first_name
from getter import get_user, save_user, get_user_status, get_daily_stat
from states import EnterUserSG, StartSG, WatchDailyStatSG
from utils import switch_to_main_menu, switch_to_add_user, switch_to_watch_daily_stat

start_dialog = Dialog(
    Window(
        Format('Привет, {username}!'),
        Const('У тебя есть админские права, кайфуй, бро😎', when='admin'),
        Format('Ошибка {error_message}', when='error'),
        Const('Вы не админ, сюда нельзя😥', when='not_admin'),
        Row(
            Button(Const('Посмотреть статистику за сегодня'), id='daily_stat', when='admin',
                   on_click=switch_to_watch_daily_stat),
        ),
        Row(
            Button(Const('Добавить юзера'), id='add_user', when='admin', on_click=switch_to_add_user),
        ),

        getter=get_user_status,
        state=StartSG.start
    )
)

enter_user_dialog = Dialog(
    Window(
        Const(text='<b>Введите id юзера</b> (id не должен повторяться! Обязательно проверьте через бд перед '
                   'созданием. В '
                   'случае повторения id ошибки не будет, но пользователь новый не создастся, так что будьте '
                   'внимательными)'),
        TextInput(
            id='id_input',
            type_factory=id_check,
            on_success=correct_id,
            on_error=error_id,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
        state=EnterUserSG.enter_id,
    ),
    Window(
        Const(text='<b>Введите имя</b> (не обязательно)'),
        TextInput(
            id='first_name_input',
            type_factory=descr_check,
            on_success=correct_first_name,
            on_error=error_first_name
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        Row(
            Back(Const('◀ назад'), id='back1'),
            Button(Const('Пропустить ▶'), id='next1', on_click=skip_input_first_name),
            Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
        ),
        state=EnterUserSG.enter_first_name,
    ),
    Window(
        Const(text='<b>Введите фамилию</b> (не обязательно)'),
        TextInput(
            id='last_name_input',
            type_factory=descr_check,
            on_success=correct_last_name,
            on_error=error_first_name
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        Row(
            Back(Const('◀ назад'), id='back2'),
            Button(Const('Пропустить ▶'), id='next2', on_click=skip_input_last_name),
            Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
        ),
        state=EnterUserSG.enter_last_name,
    ),
    Window(
        Const(text='<b>Введите username</b> (не обязательно)'),
        TextInput(
            id='username_input',
            type_factory=descr_check,
            on_success=correct_username,
            on_error=error_first_name
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        Row(
            Back(Const('◀ назад'), id='back3'),
            Button(Const('Пропустить ▶'), id='next3', on_click=skip_input_username),
            Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
        ),
        state=EnterUserSG.enter_username,
    ),
    Window(
        Format(text='<b>{id}</b>\n\n{first_name}\n{last_name}\n{username}'),
        Row(
            Back(Const('◀️назад'), id='back4'),
            Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
            Next(Const('Сохранить✅'), id='button_save')
        ),
        getter=get_user,
        state=EnterUserSG.enter_finish,
    ),
    Window(
        Const(text='<b>Пользователь успешно создан</b>', when='success'),
        Format(text='<b>id: {user_id}</b>\n\nФИО: {fio}\nusername: {username}', when='success'),
        Format(text='Ошибка {error_message}', when='error'),
        Button(Const('📃В главное меню'), id='to_main_menu', on_click=switch_to_main_menu),
        getter=save_user,
        state=EnterUserSG.enter_after_finish
    )
)

watch_daily_stat_dialog = Dialog(
    Window(
        Format(text="📊 Статистика на сегодня:\n\n"
                    "👥 Количество пользователей: {count_of_all_users}\n"
                    "🆕 Пользователей зарегистрировано сегодня: {users_registered_today}\n"
                    "📈 Онлайн сегодня: {online_peak}", when='success'),
        Format(
            text="{error_message}", when='error'
        ),
        Button(Const('📃В главное меню'), id='to_main_menu', on_click=switch_to_main_menu),
        getter=get_daily_stat,
        state=WatchDailyStatSG.start
    )
)
