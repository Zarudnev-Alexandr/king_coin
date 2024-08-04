import hashlib
import hmac
import json

from environs import Env
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.user import get_user


env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')


def verify_telegram_signature(data: dict, bot_token: str) -> bool:
    check_string = '\n'.join(f'{k}={v}' for k, v in sorted(data.items()) if k != 'hash')
    secret_key = hmac.new(bot_token.encode(), 'WebAppData'.encode(), hashlib.sha256).digest()
    expected_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
    return expected_hash == data.get('hash')

async def decode_init_data(initData: str, db: AsyncSession):
    try:
        decoded_data = json.loads(initData)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in header initData")

    # Проверяем подпись
    if not verify_telegram_signature(decoded_data, BOT_TOKEN):
        raise HTTPException(status_code=400, detail="Invalid signature")

    user_data = decoded_data.get("user", {})
    tg_id = user_data.get("id")
    username = user_data.get("username", "")
    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")
    is_premium = user_data.get("is_premium", False)

    if not tg_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    user = await get_user(db, tg_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    data_from_init_data = {
        "tg_id": tg_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "invited_tg_id": decoded_data.get("invited_tg_id", None),
        "is_premium": is_premium,
        "user": user
    }

    return data_from_init_data
