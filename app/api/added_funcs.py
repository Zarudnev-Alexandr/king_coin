import hashlib
import hmac
import json
import urllib

from environs import Env
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.user import get_user


env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

import urllib.parse
import hashlib
import hmac


# Transforms Telegram.WebApp.initData string into object
# Раскрытие строки initData
def transform_init_data(init_data: str):
    res = dict(urllib.parse.parse_qs(init_data))
    for key, value in res.items():
        res[key] = value[0]
    return res


# Валидация данных
def validate(data: dict, bot_token: str):
    check_string = "\n".join(
        sorted(f"{key}={value}" for key, value in data.items() if key != "hash"))
    secret = hmac.new(key=b'WebAppData', msg=bot_token.encode(), digestmod=hashlib.sha256)
    signature = hmac.new(key=secret.digest(), msg=check_string.encode(), digestmod=hashlib.sha256)

    return hmac.compare_digest(data['hash'], signature.hexdigest())


# Основная функция обработки данных
async def decode_init_data(initData: str, db: AsyncSession):
    try:
        parsed_data = transform_init_data(initData)
        # Преобразование строки user из JSON в словарь
        if "user" in parsed_data:
            parsed_data["user"] = json.loads(parsed_data["user"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid data format: {str(e)}")

    # Проверяем подпись
    # if not validate(parsed_data, BOT_TOKEN):
    #     raise HTTPException(status_code=400, detail="Invalid signature")

    user_data = parsed_data.get("user", {})
    tg_id = user_data.get("id")
    username = user_data.get("username", "")
    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")
    is_premium = user_data.get("is_premium", False)

    if not tg_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    user = await get_user(db, tg_id)
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")

    data_from_init_data = {
        "tg_id": tg_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "invited_tg_id": parsed_data.get("invited_tg_id", None),
        "is_premium": is_premium,
        "user": user if user else None
    }


    return data_from_init_data
