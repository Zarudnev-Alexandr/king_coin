import asyncio
import hashlib
import hmac
import json
import urllib
from datetime import datetime

from environs import Env
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.upgrade import get_user_upgrades, get_upgrade_by_id
from app.cruds.user import get_user
from app.models import Level

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


async def user_check_and_update(initData: str, db: AsyncSession):
    referral_rewards = {
        2: {"no_premium": 15000, "premium": 25000},
        3: {"no_premium": 35000, "premium": 55000},
        4: {"no_premium": 40000, "premium": 65000},
        5: {"no_premium": 65000, "premium": 90000},
        6: {"no_premium": 95000, "premium": 140000},
        7: {"no_premium": 200000, "premium": 400000},
        8: {"no_premium": 500000, "premium": 1000000},
        9: {"no_premium": 1500000, "premium": 3000000},
        10: {"no_premium": 3500000, "premium": 6000000},
    }

    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    current_time = datetime.utcnow()
    last_login = user.last_login or current_time
    time_diff = current_time - last_login

    hours_passed = min(time_diff.total_seconds() / 3600, 3)

    user_upgrades = await get_user_upgrades(user.tg_id, db)
    upgrades = await asyncio.gather(
        *[get_upgrade_by_id(db, user_upgrade.upgrade_id) for user_upgrade in user_upgrades]
    )

    total_hourly_income = sum(
        next((lvl.factor for lvl in upgrade.levels if lvl.lvl == user_upgrade.lvl), 0)
        for user_upgrade, upgrade in zip(user_upgrades, upgrades)
    )

    total_income = total_hourly_income * hours_passed

    user.money += total_income
    user.last_login = current_time

    await db.commit()
    await db.refresh(user)

    levels = await db.execute(select(Level).order_by(Level.lvl))
    levels = levels.unique().scalars().all()

    levels_list = [level for level in levels if level.lvl > user.lvl]
    info_about_user_upgrade_lvl = {}

    for level in levels_list:
        await db.refresh(level)
        if user.money >= level.required_money and user.lvl < level.lvl:
            old_lvl = user.lvl
            user.lvl = level.lvl
            user.taps_for_level = level.taps_for_level
            await db.commit()
            await db.refresh(user)

            # Начисление бонусов пригласившему
            if user.invited_tg_id:
                inviter = await get_user(db, user.invited_tg_id)
                if inviter:
                    reward = referral_rewards.get(user.lvl, {}).get("premium" if user.is_premium else "no_premium", 0)
                    inviter.money += reward
                    await db.commit()

            await db.refresh(user)

            info_about_user_upgrade_lvl = {"event": "new_lvl", "data": {"old_lvl": old_lvl,
                                                                        "new_lvl": user.lvl,
                                                                        "new_taps_for_lvl": user.taps_for_level}}
    return {"money": user.money,
            "total_hourly_income": total_hourly_income,
            "total_income": total_income,
            "hours_passed": hours_passed,
            "info": info_about_user_upgrade_lvl if info_about_user_upgrade_lvl else None
            }


async def user_check_and_update_only_money(initData: str, db: AsyncSession):
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    current_time = datetime.utcnow()
    last_login = user.last_login or current_time
    time_diff = current_time - last_login

    hours_passed = min(time_diff.total_seconds() / 3600, 3)

    user_upgrades = await get_user_upgrades(user.tg_id, db)
    upgrades = await asyncio.gather(
        *[get_upgrade_by_id(db, user_upgrade.upgrade_id) for user_upgrade in user_upgrades]
    )

    total_hourly_income = sum(
        next((lvl.factor for lvl in upgrade.levels if lvl.lvl == user_upgrade.lvl), 0)
        for user_upgrade, upgrade in zip(user_upgrades, upgrades)
    )

    total_income = total_hourly_income * hours_passed

    user.money += total_income
    user.last_login = current_time

    await db.commit()
    await db.refresh(user)

    return {"money": user.money,
            "total_hourly_income": total_hourly_income,
            "total_income": total_income,
            "hours_passed": hours_passed,
            }


async def user_check_and_update_without_init_data(user, db: AsyncSession):
    referral_rewards = {
        2: {"no_premium": 15000, "premium": 25000},
        3: {"no_premium": 35000, "premium": 55000},
        4: {"no_premium": 40000, "premium": 65000},
        5: {"no_premium": 65000, "premium": 90000},
        6: {"no_premium": 95000, "premium": 140000},
        7: {"no_premium": 200000, "premium": 400000},
        8: {"no_premium": 500000, "premium": 1000000},
        9: {"no_premium": 1500000, "premium": 3000000},
        10: {"no_premium": 3500000, "premium": 6000000},
    }

    current_time = datetime.utcnow()
    last_login = user.last_login or current_time
    time_diff = current_time - last_login

    hours_passed = min(time_diff.total_seconds() / 3600, 3)

    user_upgrades = await get_user_upgrades(user.tg_id, db)
    upgrades = await asyncio.gather(
        *[get_upgrade_by_id(db, user_upgrade.upgrade_id) for user_upgrade in user_upgrades]
    )

    total_hourly_income = sum(
        next((lvl.factor for lvl in upgrade.levels if lvl.lvl == user_upgrade.lvl), 0)
        for user_upgrade, upgrade in zip(user_upgrades, upgrades)
    )

    total_income = total_hourly_income * hours_passed

    user.money += total_income
    user.last_login = current_time

    await db.commit()
    await db.refresh(user)

    levels = await db.execute(select(Level).order_by(Level.lvl))
    levels = levels.unique().scalars().all()

    levels_list = [level for level in levels if level.lvl > user.lvl]
    info_about_user_upgrade_lvl = {}

    for level in levels_list:
        await db.refresh(level)
        if user.money >= level.required_money and user.lvl < level.lvl:
            old_lvl = user.lvl
            user.lvl = level.lvl
            user.taps_for_level = level.taps_for_level
            await db.commit()
            await db.refresh(user)

            # Начисление бонусов пригласившему
            if user.invited_tg_id:
                inviter = await get_user(db, user.invited_tg_id)
                if inviter:
                    reward = referral_rewards.get(user.lvl, {}).get("premium" if user.is_premium else "no_premium", 0)
                    inviter.money += reward
                    await db.commit()

            await db.refresh(user)

            info_about_user_upgrade_lvl = {"event": "new_lvl", "data": {"old_lvl": old_lvl,
                                                                        "new_lvl": user.lvl,
                                                                        "new_taps_for_lvl": user.taps_for_level}}
    return {"money": user.money,
            "total_hourly_income": total_hourly_income,
            "total_income": total_income,
            "hours_passed": hours_passed,
            "info": info_about_user_upgrade_lvl if info_about_user_upgrade_lvl else None
            }


async def user_check_and_update_without_init_data_only_money(user, db: AsyncSession):
    current_time = datetime.utcnow()
    last_login = user.last_login or current_time
    time_diff = current_time - last_login

    hours_passed = min(time_diff.total_seconds() / 3600, 3)

    user_upgrades = await get_user_upgrades(user.tg_id, db)
    upgrades = await asyncio.gather(
        *[get_upgrade_by_id(db, user_upgrade.upgrade_id) for user_upgrade in user_upgrades]
    )

    total_hourly_income = sum(
        next((lvl.factor for lvl in upgrade.levels if lvl.lvl == user_upgrade.lvl), 0)
        for user_upgrade, upgrade in zip(user_upgrades, upgrades)
    )

    total_income = total_hourly_income * hours_passed

    user.money += total_income
    user.last_login = current_time

    await db.commit()
    await db.refresh(user)

    return {"money": user.money,
            "total_hourly_income": total_hourly_income,
            "total_income": total_income,
            "hours_passed": hours_passed,
            }
