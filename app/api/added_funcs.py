import json

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.user import get_user


async def decode_init_data(initData: str, db: AsyncSession):
    try:
        decoded_data = json.loads(initData)

        data = decoded_data
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in header initData")

    data_from_init_data = {
        "tg_id": data.get("id"),
        "username": data.get("username", ""),
        "first_name": data.get("first_name", ""),
        "last_name": data.get("last_name", ""),
        "invited_tg_id": data.get("invited_tg_id", None),
    }

    if not data_from_init_data["tg_id"]:
        raise HTTPException(status_code=400, detail="User ID is required")

    user = await get_user(db, data_from_init_data["tg_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    data_from_init_data["user"] = user
    return data_from_init_data
