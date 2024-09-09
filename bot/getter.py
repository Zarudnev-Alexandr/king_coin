import json
import urllib.parse

import aiohttp
import requests
from aiogram.types import User
from aiogram_dialog import DialogManager
from environs import Env

env = Env()
env.read_env()

API_URL = env('API_URL')


async def get_user(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    return {'id': dialog_manager.dialog_data['id'],
            'first_name': dialog_manager.dialog_data['first_name'] or '',
            'last_name': dialog_manager.dialog_data['last_name'] or '',
            'username': dialog_manager.dialog_data['username'] or '',
            }


async def save_user(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    user_data = {'id': int(dialog_manager.dialog_data['id']),
                 'first_name': dialog_manager.dialog_data['first_name'] or '',
                 'last_name': dialog_manager.dialog_data['last_name'] or '',
                 'username': dialog_manager.dialog_data['username'] or '',
                 "language_code": "ru",
                 "allows_write_to_pm": True
                 }

    user_json = json.dumps(user_data)

    user_encoded = urllib.parse.quote(user_json)

    init_data = f"query_id=AAEHkPY1AAAAAAeQ9jVyoovM&user={user_encoded}&auth_date=1722771586&hash=472c999c56fe21e642b74eba904291cf53e2e5b8eff575feeb7991248b16672e"

    headers = {
        'accept': 'application/json',
        'initData': init_data
    }

    response = requests.post(f'{API_URL}/api/users/logreg', headers=headers)

    try:
        response_data = response.json()
        await event_from_user.bot.send_message(event_from_user.id,
                                               text=f"https://t.me/KingCoin_ebot/launch?startapp="
                                                    f"{response_data['tg_id']}\n"
                                                    f"Здесь будет приветсвенный текст")
        return {'user_id': response_data['tg_id'],
                'fio': response_data['fio'],
                'username': response_data['username'],
                'success': True,
                }
    except Exception as e:
        return {'error': True, 'error_message': e}


async def get_user_status(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    tg_id = event_from_user.id

    backend_url = f'{API_URL}/api/users/get_user_status/{tg_id}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(backend_url) as response:
                if response.status == 200:
                    if await response.json():
                        return {'admin': True, 'username': event_from_user.username}
                    else:
                        return {'not_admin': True, 'username': event_from_user.username}
    except Exception as e:
        return {'error': True, 'username': event_from_user.username, 'error_message': f"Не удалось разобрать ответ "
                                                                                      f"сервера: {e}"}


async def get_daily_stat(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    tg_id = event_from_user.id

    backend_url = f'{API_URL}/api/users/daily_stats'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(backend_url, params={"tg_id": tg_id}) as response:
                if response.status == 404:
                    return {'error': True, 'error_message': 'Пользователь не найден.'}
                elif response.status == 403:
                    return {'error': True, 'error_message': 'У вас нет прав для использования этого API.'}
                elif response.status != 200:
                    return {'error': True, 'error_message': 'Произошла ошибка при запросе к серверу'}
                data = await response.json()

                return {
                    'success': True,
                    'count_of_all_users': data['count_of_all_users'],
                    'users_registered_today': data['users_registered_today'],
                    'online_peak': data['online_peak'],
                }

    except Exception as e:
        return {'error': True, 'error_message': f'Произошла ошибка {e}'}

