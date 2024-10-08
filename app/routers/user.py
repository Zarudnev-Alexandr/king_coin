import asyncio
import json
from datetime import datetime, timedelta
from typing import Optional

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError
from fastapi import APIRouter, Depends, HTTPException, Path, Header, Query
from sqlalchemy import func, select, update, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.user import get_user, create_user, get_user_boost, get_boost_by_id, add_boost, \
    get_boost_by_lvl, get_next_boost, upgrade_user_boost, get_user_bool, get_daily_reward, add_daily_reward, \
    update_user_level, get_daily_reward_all, get_count_of_all_users, get_all_earned_money, get_users_registered_today, \
    get_online_peak_today
from ..api.added_funcs import decode_init_data, transform_init_data, validate, user_check_and_update, \
    user_check_and_update_only_money, log_execution_time
from ..config import loop, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP, KAFKA_TOPIC
from ..cruds.upgrade import get_user_upgrades, get_upgrade_by_id, get_user_upgrades_with_levels
from ..database import get_db, sessionmanager, CurrentAsyncSession
from ..models import DailyReward, User, UserAdWatch
from ..schemas import Message, UserCreate, UserBase, BoostCreateSchema, DailyRewardResponse, CreateDailyRewardSchema, \
    InitDataSchema, GameResultsSchema
from ..websockets.settings import ws_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_route = APIRouter()


# @user_route.post('/create_message')
# async def send(message: Message):
#     producer = AIOKafkaProducer(
#         loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
#     await producer.start()
#     try:
#         value_json = json.dumps(message.__dict__).encode('utf-8')
#         await producer.send_and_wait(topic=KAFKA_TOPIC, value=value_json)
#     finally:
#         await producer.stop()
#
#
# async def consume():
#     try:
#         consumer = AIOKafkaConsumer(KAFKA_TOPIC,
#                                     loop=loop,
#                                     bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
#                                     group_id=KAFKA_CONSUMER_GROUP)
#     except KafkaError as err:
#         raise Exception(f"🥰🥰🥰{err}")
#
#     await consumer.start()
#     try:
#
#         async for msg in consumer:
#             logger.info(f'Consumer msg😍😍😍😍😍😍: {msg}')
#     except Exception as e:
#         logger.info(f"Error consuming messages: {e}")
#     finally:
#         await consumer.stop()


# @user_route.post('/user')
# async def register_send(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     producer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
#     await producer.start()
#
#     try:
#         user = await get_user(db, tg_id=user.tg_id)
#         if user:
#             raise HTTPException(status_code=400, detail="User already registered")
#
#         # Собираем сообщение для Kafka
#         message = {
#             "tg_id": user.tg_id,
#             "username": user.username,
#             "fio": user.fio,
#             "invited_tg_id": user.invited_tg_id
#         }
#         value_json = json.dumps(message).encode('utf-8')
#         await producer.send_and_wait(topic="user_registration", value=value_json)
#
#         return {"status": "User registration message sent to Kafka"}
#
#     finally:
#         await producer.stop()
#
#
# async def consume_register():
#     consumer = AIOKafkaConsumer(
#         "user_registration",
#         loop=loop,
#         bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
#         group_id="registration_group"
#     )
#
#     await consumer.start()
#     try:
#         async for msg in consumer:
#             logger.info(f'Received message: {msg.value.decode("utf-8")}')
#             message = json.loads(msg.value.decode("utf-8"))
#             user_data = UserCreate(**message)
#
#             async with await get_db() as db:
#                 await create_user(db, user_data)
#                 await db.commit()
#     except Exception as e:
#         logger.info(f"Error consuming messages: {e}")
#     finally:
#         await consumer.stop()


# @user_route.post('/user')
# async def register_send(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     user = await get_user(db, tg_id=user.tg_id)
#     if user:
#         raise HTTPException(status_code=400, detail="User already registered")
#
#     message = {
#         "tg_id": user.tg_id,
#         "username": user.username,
#         "fio": user.fio,
#         "invited_tg_id": user.invited_tg_id
#     }
#
#     # user_data = UserCreate(**message)
#     new_user = await create_user(db, **message)
#     if not new_user:
#         raise HTTPException(status_code=500, detail="Error")
#
#     return new_user
#
#
# @user_route.post('/user-login')
# async def user_login(user_id: int, db: AsyncSession = Depends(get_db)) -> dict:
#     user = await get_user(db, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     current_time = datetime.utcnow()
#     last_login = user.last_login or current_time
#     time_diff = current_time - last_login
#
#     # Ограничиваем расчет дохода максимум 3 часами
#     hours_passed = min(time_diff.total_seconds() / 3600, 3)
#
#     # Получаем все улучшения пользователя
#     user_upgrades = await get_user_upgrades(user_id, db)
#
#     # Получаем все апгрейды пользователя асинхронно
#     upgrades = await asyncio.gather(
#         *[get_upgrade_by_id(db, user_upgrade.upgrade_id) for user_upgrade in user_upgrades]
#     )
#
#     # Рассчитываем общий доход в час
#     total_hourly_income = sum(
#         next((lvl.factor for lvl in upgrade.levels if lvl.lvl == user_upgrade.lvl), 0)
#         for user_upgrade, upgrade in zip(user_upgrades, upgrades)
#     )
#
#     # Рассчитываем доход за прошедшее время
#     total_income = total_hourly_income * hours_passed
#
#     # Обновляем баланс пользователя
#     user.money += total_income
#
#     # Обновляем дату последнего входа
#     user.last_login = current_time
#
#     # Получаем текущий буст пользователя
#     user_boost = await get_user_boost(db, user_id)
#
#     if user_boost:
#         boost = await get_boost_by_id(db, user_boost.boost_id)
#         if boost:
#             boost_data = {
#                 "boost_id": boost.lvl,
#                 "name": boost.name,
#                 "price": boost.price,
#                 "lvl": boost.lvl,
#                 "tap_boost": boost.tap_boost,
#                 "one_tap": boost.one_tap,
#                 "pillars_10": boost.pillars_10,
#                 "pillars_30": boost.pillars_30,
#                 "pillars_100": boost.pillars_100
#             }
#         else:
#             boost_data = {}
#     else:
#         boost_data = {}
#     logger.info('🐟', boost_data)
#
#     await db.commit()
#     await db.refresh(user)
#
#     # Преобразуем объект user в словарь
#     user_data = UserBase.from_orm(user).dict()
#     user_data["total_income"] = total_income
#     user_data["boost"] = boost_data
#
#     return user_data


@user_route.post('/logreg')
async def logreg(initData: str = Header(...), ref: Optional[str] = Query(None), db: AsyncSession = Depends(get_db)):
    logger.info(f"**logreg**---------------------")
    if ref == "None":
        ref = None
    else:
        try:
            ref = int(ref) if ref is not None else None
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ref parameter")

    data_from_init_data = await log_execution_time(decode_init_data)(initData, db)

    tg_id = data_from_init_data["tg_id"]
    username = data_from_init_data["username"]
    first_name = data_from_init_data["first_name"]
    last_name = data_from_init_data["last_name"]
    is_premium = data_from_init_data["is_premium"]
    user = data_from_init_data["user"]

    if user:
        current_time = datetime.utcnow()
        last_login = user.last_login or current_time
        time_diff = current_time - last_login
        hours_passed = min(time_diff.total_seconds() / 3600, 3)

        user_upgrades = await log_execution_time(get_user_upgrades)(tg_id, db)

        upgrades = await log_execution_time(asyncio.gather)(
            *[get_upgrade_by_id(db, user_upgrade.upgrade_id) for user_upgrade in user_upgrades]
        )

        total_hourly_income = sum(
            next((lvl.factor for lvl in upgrade.levels if lvl.lvl == user_upgrade.lvl), 0)
            for user_upgrade, upgrade in zip(user_upgrades, upgrades)
        )

        total_income = total_hourly_income * hours_passed
        user.money += total_income
        user.last_login = current_time

        user_boost = await log_execution_time(get_user_boost)(db, tg_id)

        if user_boost:
            current_boost = await log_execution_time(get_boost_by_id)(db, user_boost.boost_id)

            if current_boost:
                boost_data = {
                    "boost_id": current_boost.lvl,
                    "name": current_boost.name,
                    "price": current_boost.price,
                    "lvl": current_boost.lvl,
                    "tap_boost": current_boost.tap_boost,
                    "one_tap": current_boost.one_tap,
                    "pillars_2": current_boost.pillars_2,
                    "pillars_10": current_boost.pillars_10,
                    "pillars_30": current_boost.pillars_30,
                    "pillars_100": current_boost.pillars_100
                }

                next_boost = await log_execution_time(get_next_boost)(db, current_boost.lvl)

                next_boost_data = {
                    "boost_id": next_boost.lvl,
                    "name": next_boost.name,
                    "price": next_boost.price,
                    "lvl": next_boost.lvl,
                    "tap_boost": next_boost.tap_boost,
                    "pillars_2": current_boost.pillars_2,
                    "pillars_10": next_boost.pillars_10,
                    "pillars_30": next_boost.pillars_30,
                    "pillars_100": next_boost.pillars_100
                } if next_boost else None
            else:
                boost_data = {}
                next_boost_data = None
        else:
            boost_data = {}
            next_boost_data = None

        next_level = await log_execution_time(update_user_level)(db, user)

        next_level_data = {
            "lvl": next_level.lvl if next_level else None,
            "required_money": next_level.required_money if next_level else None,
            "taps_for_level": next_level.taps_for_level if next_level else None,
            "money_to_get_the_next_boost": next_level.required_money - user.money if next_level and next_level.required_money else None
        } if next_level else {}

        await log_execution_time(db.commit)()
        # await log_execution_time(db.refresh)(user)

        user_data = {
            "tg_id": user.tg_id,
            "username": user.username,
            "fio": user.fio,
            "last_login": user.last_login,
            "money": user.money,
            "user_lvl": user.lvl,
            "taps_for_level": user.taps_for_level,
            "earnings_per_hour": total_hourly_income,
            "total_income": total_income,
            "boost": boost_data,
            "next_boost": next_boost_data,
            "next_level_data": next_level_data
        }

        return user_data
    else:
        # Пользователь не найден, выполняем регистрацию
        new_user = await create_user(
            db,
            tg_id=tg_id,
            username=username,
            fio=first_name + ' ' + last_name,
            invited_tg_id=ref,
            is_premium=is_premium
        )
        if not new_user:
            raise HTTPException(status_code=500, detail="Error creating user")

        # Начисление бонусных монет
        bonus = 5000
        if ref:
            bonus = 15000
            if is_premium:
                bonus = 25000
        new_user.user.money += bonus
        await db.commit()
        await db.refresh(new_user)

        if ref:
            inviter = await get_user(db, ref)
            if inviter:
                inviter.money += bonus
                await db.commit()
                await db.refresh(inviter)

        await db.refresh(new_user)
        boost_data = {
            "boost_id": new_user.boost.lvl,
            "name": new_user.boost.name,
            "price": new_user.boost.price,
            "lvl": new_user.boost.lvl,
            "tap_boost": new_user.boost.tap_boost,
            "one_tap": new_user.boost.one_tap,
            "pillars_2": new_user.boost.pillars_2,
            "pillars_10": new_user.boost.pillars_10,
            "pillars_30": new_user.boost.pillars_30,
            "pillars_100": new_user.boost.pillars_100
        } if new_user.boost else {}

        next_boost = await get_next_boost(db, new_user.boost.lvl)
        next_boost_data = {
            "boost_id": next_boost.lvl,
            "name": next_boost.name,
            "price": next_boost.price,
            "lvl": next_boost.lvl,
            "tap_boost": next_boost.tap_boost,
            "one_tap": next_boost.one_tap,
            "pillars_2": next_boost.pillars_2,
            "pillars_10": next_boost.pillars_10,
            "pillars_30": next_boost.pillars_30,
            "pillars_100": next_boost.pillars_100
        } if next_boost else None

        next_level = await update_user_level(db, new_user.user)
        if next_level:
            await db.refresh(next_level)
        await db.refresh(new_user)
        next_level_data = {
            "next_lvl": next_level.lvl if next_level else None,
            "required_money": next_level.required_money if next_level else None,
            "taps_for_level": next_level.taps_for_level if next_level else None,
            "money_to_get_the_next_boost": next_level.required_money - new_user.user.money if next_level and next_level.required_money else None
        } if next_level else {}

        user_data = {
            "tg_id": new_user.user.tg_id,
            "username": new_user.user.username,
            "fio": new_user.user.fio,
            "last_login": new_user.user.last_login,
            "money": new_user.user.money,
            "user_lvl": new_user.user.lvl,
            "taps_for_level": new_user.user.taps_for_level,
            "earnings_per_hour": 0,
            "boost": boost_data,
            "next_boost": next_boost_data,
            "next_level_data": next_level_data,
            "is_registred": True
        }

        await db.close()
        return user_data


# @user_route.post('/boost')
# async def create_upgrade(boost_create: BoostCreateSchema,
#                          db: AsyncSession = Depends(get_db)):
#     user_data = {
#         'name': boost_create.name,
#         'lvl': boost_create.lvl,
#         "price": boost_create.price,
#         'tap_boost': boost_create.tap_boost,
#         'one_tap': boost_create.one_tap,
#         'pillars_2': boost_create.pillars_2,
#         'pillars_10': boost_create.pillars_10,
#         'pillars_30': boost_create.pillars_30,
#         'pillars_100': boost_create.pillars_100
#     }
#
#     boost = await get_boost_by_lvl(db, boost_lvl=boost_create.lvl)
#
#     if boost:
#         raise HTTPException(status_code=409, detail="this lvl is already in use")
#
#     new_boost = await add_boost(db, **user_data)
#     if new_boost:
#         return new_boost
#     else:
#         raise HTTPException(status_code=400, detail="failed to create boost")


@user_route.post('/upgrade-boost')
async def upgrade_boost(initData: str = Header(...), db: AsyncSession = Depends(get_db)):
    logger.info(f"**upgrade_boost**---------------------")
    """
    Улучшаем буст
    """
    init_data_decode = await log_execution_time(decode_init_data)(initData, db)
    user = init_data_decode["user"]

    await log_execution_time(user_check_and_update_only_money)(initData, db)

    user_boost = await log_execution_time(get_user_boost)(db, user.tg_id)
    if not user_boost:
        raise HTTPException(status_code=404, detail="User boost not found")

    current_boost = await log_execution_time(get_boost_by_id)(db, user_boost.boost_id)
    if not current_boost:
        raise HTTPException(status_code=404, detail="Current boost not found")

    next_boost = await log_execution_time(get_next_boost)(db, current_boost.lvl)
    if not next_boost:
        user_check = await log_execution_time(user_check_and_update)(initData, db)
        # Если следующего буста нет, возвращаем текущий статус с флагом "буст на максимальном уровне"
        response = {
            "user_id": user_boost.user_id,
            "boost_id": user_boost.boost_id,
            "user_money": user.money,
            "next_boost": None,
            "boost_at_max_level": True,
            "user_check": user_check
        }
        return response

    if user.money < next_boost.price:
        raise HTTPException(status_code=400, detail="Not enough money to upgrade boost")

    new_user_boost = await log_execution_time(upgrade_user_boost)(db, user_boost, user, next_boost)
    if not new_user_boost:
        raise HTTPException(status_code=500, detail="Failed to improve boost")

    # Получаем следующий уровень буста после обновления
    next_boost_after_bought = await log_execution_time(get_next_boost)(db, next_boost.lvl)

    next_boost_after_bought_dict = {
        "lvl": next_boost_after_bought.lvl if next_boost_after_bought else None,
        "price": next_boost_after_bought.price if next_boost_after_bought else None,
        "tap_boost": next_boost_after_bought.tap_boost if next_boost_after_bought else None,
        "one_tap": next_boost_after_bought.one_tap if next_boost_after_bought else None,
        "pillars_2": next_boost_after_bought.pillars_2 if next_boost_after_bought else None,
        "pillars_10": next_boost_after_bought.pillars_10 if next_boost_after_bought else None,
        "pillars_30": next_boost_after_bought.pillars_30 if next_boost_after_bought else None,
        "pillars_100": next_boost_after_bought.pillars_100 if next_boost_after_bought else None,
    }

    user_check = await log_execution_time(user_check_and_update)(initData, db)

    response = {
        "user_id": user_boost.user_id,
        "boost_id": user_boost.boost_id,
        "user_money": user.money,
        "next_boost": next_boost_after_bought_dict if next_boost_after_bought else None,
        "boost_at_max_level": next_boost_after_bought is None,
        "user_check": user_check
    }

    return response


@user_route.get("/next-upgrade")
async def get_next_upgrade_func(initData: str = Header(...),
                                db: AsyncSession = Depends(get_db)) -> BoostCreateSchema:
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    user_boost = await get_user_boost(db, user.tg_id)

    if not user_boost:
        raise HTTPException(status_code=404, detail="User boost not found")

    # Получаем текущий и следующий уровни буста
    current_boost = await get_boost_by_id(db, user_boost.boost_id)

    if not current_boost:
        raise HTTPException(status_code=404, detail="Current boost not found")

    next_boost = await get_next_boost(db, current_boost.lvl)

    if not next_boost:
        raise HTTPException(status_code=404, detail="Next boost level not found")

    return next_boost


@user_route.post('/claim-daily-reward')
async def claim_daily_reward_api(initData: str = Header(...), db: AsyncSession = Depends(get_db)):
    """
    Получаем дневную награду
    """
    init_data_decode = await log_execution_time(decode_init_data)(initData, db)
    user = init_data_decode["user"]

    await user_check_and_update_only_money(initData, db)

    current_time = datetime.utcnow()
    received_last_daily_reward = user.received_last_daily_reward or current_time

    # Проверка, прошло ли более одного дня с последнего входа
    if current_time > received_last_daily_reward + timedelta(days=2):
        user.days_in_row = 0

    # Проверка, прошло ли менее одного дня с последнего входа
    if current_time < received_last_daily_reward + timedelta(hours=24):
        raise HTTPException(status_code=200, detail="less than one day has passed")

    # Определение текущего дня награды
    reward_day = user.days_in_row + 1

    # Получение награды
    daily_reward = await get_daily_reward(db, reward_day)
    if not daily_reward:
        user.days_in_row = 1
        reward_day = 1
        daily_reward = await get_daily_reward(db, reward_day)
        # raise HTTPException(status_code=404, detail="Reward for the day not found")

    # Обновление пользователя
    user.money += daily_reward.reward
    user.days_in_row = reward_day
    user.received_last_daily_reward = current_time

    # Сброс дней в ряду, если награды закончились
    max_reward_day = (await db.execute(select(func.max(DailyReward.day)))).scalar()
    if user.days_in_row >= max_reward_day:
        user.days_in_row = 0

    user_check = await user_check_and_update(initData, db)
    await db.commit()
    await db.refresh(user)
    await db.refresh(daily_reward)

    return {"day": daily_reward.day,
            "reward": daily_reward.reward,
            "users_money": user.money,
            "user_check": user_check}


# @user_route.post('/create-daily-reward')
# async def create_daily_reward(daily_reward: CreateDailyRewardSchema,
#                               db: AsyncSession = Depends(get_db)):
#     user_data = {
#         'day': daily_reward.day,
#         'reward': daily_reward.reward,
#     }
#
#     old_daily_reward = await get_daily_reward(db, day=daily_reward.day)
#
#     if old_daily_reward:
#         raise HTTPException(status_code=409, detail="this day is already in use")
#
#     new_daily_reward = await add_daily_reward(db, **user_data)
#     if new_daily_reward:
#         return new_daily_reward
#     else:
#         raise HTTPException(status_code=400, detail="failed to create boost")


@user_route.get('/daily-reward')
async def get_daily_reward_api(initData: str = Header(...), db: AsyncSession = Depends(get_db)):
    """
    Получаем все дневные награды и количество просмотренных реклам за сегодня.
    """
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    last_received = user.received_last_daily_reward
    days_in_row = user.days_in_row

    # Получаем текущую дату
    today = datetime.utcnow()

    if last_received and today > last_received + timedelta(days=2):
        days_in_row = 0

    # Проверяем, была ли награда уже получена сегодня
    if last_received and today < last_received + timedelta(hours=24):
        is_collect = True
        current_day = (days_in_row % 12)
        if current_day == 0:
            current_day = 12  # Ensuring it wraps around correctly
    else:
        is_collect = False
        current_day = (days_in_row % 12) + 1

    # Получаем награду за текущий день
    daily_reward = await get_daily_reward(db, current_day)
    if not daily_reward:
        raise HTTPException(status_code=404, detail="Daily reward not found for the current day")

    # Получаем количество просмотренных реклам за сегодня
    ads_watched_today = await db.scalar(
        select(UserAdWatch).filter(UserAdWatch.user_id == user.tg_id,
                                   func.date(UserAdWatch.watched_date) == today.date())
    )

    return {
        "day": daily_reward.day,
        "is_collect": is_collect,
        "ads_watched_today": ads_watched_today.ads_watched if ads_watched_today else 0 or 0,
        "ads_reward": 10000,
        "is_ads_collected": ads_watched_today.is_collected if ads_watched_today else False,
    }


@user_route.post('/watch-ad')
async def watch_ad(initData: str = Header(...), db: AsyncSession = Depends(get_db)):
    """
    Увеличиваем счетчик просмотренных реклам и начисляем награду.
    """
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    await user_check_and_update_only_money(initData, db)

    # Получаем текущую дату и время
    today = datetime.utcnow()

    # Ищем запись о просмотрах реклам за сегодня (сравнение по дате)
    ad_watch = await db.scalar(
        select(UserAdWatch).filter(
            UserAdWatch.user_id == user.tg_id,
            func.date(UserAdWatch.watched_date) == today.date()  # Сравниваем только дату
        )
    )

    if not ad_watch:
        # Если записи нет, создаем новую
        ad_watch = UserAdWatch(user_id=user.tg_id, watched_date=today, ads_watched=1)
        db.add(ad_watch)
        user.money += 10000  # Начисляем награду за первую рекламу
    else:
        # Если запись есть, проверяем количество просмотренных реклам
        if ad_watch.ads_watched >= 3:
            raise HTTPException(status_code=400, detail="Вы уже посмотрели 3 рекламы сегодня")

        # Если количество меньше 3, увеличиваем счетчик и начисляем награду
        ad_watch.ads_watched += 1
        user.money += 10000  # Начисляем награду за каждый просмотр

    user_check = await user_check_and_update(initData, db)
    await db.commit()
    await db.refresh(ad_watch)
    await db.refresh(user)

    return {
        "ads_watched_today": ad_watch.ads_watched,
        "current_user_money": user.money,
        "is_ads_collected": ad_watch.ads_watched >= 3,
        "user_check": user_check
    }


@user_route.get('/get-referral-link')
async def get_referral_link_api(initData: str = Header(...), db: AsyncSession = Depends(get_db)):
    """
    Получаем реферальную ссылку
    """
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    referral_link = f"https://t.me/KingCoin_ebot/launch?startapp={user.tg_id}"
    return {"referral_link": referral_link}


@user_route.post('/game-result')
async def get_game_result_api(encrypted_information: GameResultsSchema,
                              initData: str = Header(...),
                              db: AsyncSession = Depends(get_db)):
    """
    Получаем результаты игры
    """
    init_data_decode = await log_execution_time(decode_init_data)(initData, db)
    user = init_data_decode["user"]

    # В будущем тут будет шифрование

    # encrypted_data = {
    #     "earned_coins": encrypted_information.encrypted_information
    # }
    earned_coins = int(encrypted_information.encrypted_information)

    user.money += earned_coins
    if user.number_of_columns_passed is None or \
            user.number_of_columns_passed < encrypted_information.number_of_columns_passed:
        user.number_of_columns_passed = encrypted_information.number_of_columns_passed
    await log_execution_time(db.commit)()
    await log_execution_time(db.refresh)(user)

    # Отправка уведомления через WebSocket
    await ws_manager.notify_user(user.tg_id, {"event": "game_result", "data": {"money_added": earned_coins,
                                                                               "users_money": user.money}})

    user_check = await log_execution_time(user_check_and_update)(initData, db)
    return {"money_added": earned_coins, "users_money": user.money, "user_check": user_check}


@user_route.get('/invited-users')
async def get_invited_users(
        initData: str = Header(...),
        db: AsyncSession = Depends(get_db)
):
    # Расшифровываем initData и получаем текущего пользователя
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    # Получаем всех приглашенных пользователей
    invited_users_query = select(User).where(User.invited_tg_id == user.tg_id)
    invited_users = await db.execute(invited_users_query)
    invited_users = invited_users.scalars().all()

    invited_users_data = []

    for invited_user in invited_users:
        # Получаем апгрейды пользователя
        user_upgrades = await get_user_upgrades(invited_user.tg_id, db)
        upgrades = await asyncio.gather(
            *[get_upgrade_by_id(db, user_upgrade.upgrade_id) for user_upgrade in user_upgrades]
        )

        # Рассчитываем общий ежечасный доход пользователя
        total_hourly_income = sum(
            next((lvl.factor for lvl in upgrade.levels if lvl.lvl == user_upgrade.lvl), 0)
            for user_upgrade, upgrade in zip(user_upgrades, upgrades)
        )

        # user_upgrades = await get_user_upgrades(invited_user.tg_id, db)
        #
        # total_hourly_income = 0
        # for user_upgrade in user_upgrades:
        #     current_lvl = user_upgrade.lvl
        #     for lvl in user_upgrade.upgrade.levels:
        #         if current_lvl == lvl.lvl:
        #             total_hourly_income += lvl.factor

        # Подсчет количества пользователей, приглашенных данным пользователем
        invited_count = await db.scalar(select(func.count()).where(User.invited_tg_id == invited_user.tg_id))

        # Определяем вознаграждение по реферальной программе
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
            # 10: {"no_premium": 10000000, "premium": 20000000},
        }

        # Определяем значение полученного вознаграждения на основе уровня и премиума
        reward_level = referral_rewards.get(invited_user.lvl, None)
        if reward_level:
            if invited_user.is_premium:
                earned_money = reward_level["premium"]
            else:
                earned_money = reward_level["no_premium"]
        else:
            earned_money = 0  # Если уровень больше 10, можно задать значение по умолчанию

        # Добавляем информацию о приглашенном пользователе в список
        invited_users_data.append({
            "tg_id": invited_user.tg_id,
            "username": invited_user.username,
            "fio": invited_user.fio,
            "lvl": invited_user.lvl,
            "money": invited_user.money,
            "total_hourly_income": total_hourly_income,
            "is_premium": invited_user.is_premium if invited_user.is_premium else None,
            "invited_count": invited_count,
            "earned_money": earned_money  # Добавляем рассчитанное значение
        })

    return {"invited_users": invited_users_data}


@user_route.delete("/delete_user")
async def delete_user(initData: str = Header(...), db: AsyncSession = Depends(get_db)):
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    await db.execute(
        update(User)
        .where(User.invited_tg_id == user.tg_id)
        .values(invited_tg_id=None)
    )

    # Удалите пользователя
    await db.execute(delete(UserAdWatch).where(UserAdWatch.user_id == user.tg_id))
    await db.delete(user)
    await db.commit()

    return {"detail": "User and all related records have been deleted"}


@user_route.get('/leaderboard')
async def get_leaderboard(
        category: str = Query(..., regex="^(columns|money|hourly_income)$"),
        initData: str = Header(...),
        db: AsyncSession = Depends(get_db)
):
    """
    Получаем топ 10 игроков в выбранной категории: количество пройденных колонн (columns),
    количество накопленных денег (money) или ежечасный доход (hourly_income).
    """
    # Декодируем данные пользователя
    data_from_init_data = await decode_init_data(initData, db)
    tg_id = data_from_init_data["tg_id"]

    # Формируем запросы для каждой категории
    if category == "columns":
        query = select(User).order_by(desc(func.coalesce(User.number_of_columns_passed, 0))).limit(10)
    elif category == "money":
        query = select(User).order_by(desc(func.coalesce(User.money, 0))).limit(10)
    else:
        raise HTTPException(status_code=400, detail="Invalid category")

    # Получаем топ 10 игроков
    top_players = await db.execute(query)
    top_players_list = top_players.scalars().all()

    # Проверяем, входит ли текущий пользователь в топ-10
    current_user = await db.get(User, tg_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_in_top = next((index for index, player in enumerate(top_players_list) if player.tg_id == tg_id), None)

    # Если пользователь в топ-10, используем этот ранг
    if user_in_top is not None:
        user_rank = user_in_top + 1
    else:
        # Иначе вычисляем ранг пользователя, если он не в топ-10
        if category == "columns":
            user_rank_query = select(func.count(User.tg_id)).where(
                func.coalesce(User.number_of_columns_passed, 0) > func.coalesce(current_user.number_of_columns_passed,
                                                                                0)
            )
        elif category == "money":
            user_rank_query = select(func.count(User.tg_id)).where(
                func.coalesce(User.money, 0) > func.coalesce(current_user.money, 0)
            )

        user_rank_result = await db.execute(user_rank_query)
        user_rank = user_rank_result.scalar() + 1  # Корректируем, чтобы начался с 1

    # Формируем список топ игроков
    leaderboard = [
        {
            "rank": index + 1,
            "tg_id": player.tg_id,
            # "username": player.username,
            "fio": player.fio,
            "lvl": player.lvl,
            "columns_passed": player.number_of_columns_passed,
            "money": player.money,
        }
        for index, player in enumerate(top_players_list)
    ]

    # Формируем данные текущего пользователя
    current_user_data = {
        "rank": user_rank,
        "tg_id": current_user.tg_id,
        # "username": current_user.username,
        "fio": current_user.fio,
        "lvl": current_user.lvl,
        "columns_passed": current_user.number_of_columns_passed,
        "money": current_user.money,
    }

    return {"leaderboard": leaderboard, "current_user": current_user_data}


@user_route.get("/get_current_user_state")
async def get_current_user_state(initData: str = Header(...), db: AsyncSession = Depends(get_db)):
    user_check = await user_check_and_update(initData, db)
    if user_check:
        return user_check


@user_route.get("/daily_stats")
async def all_users_count(tg_id: int, db: AsyncSession = Depends(get_db)):
    """
    Считаем дневную статистику:
    1) количество пользоватлей всего
    2) всего монет заработано
    3) количество юзеров за сегодня
    """

    user = await get_user(db, tg_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Вы не админ, чтобы пользоваться этим API")

    count_of_all_users = await get_count_of_all_users(db)
    # all_earned_money = await get_all_earned_money(db)
    users_registered_today = await get_users_registered_today(db)
    today_online_peak = await get_online_peak_today(db)

    return {
        "count_of_all_users": count_of_all_users,
        # "all_earned_money": int(all_earned_money),
        "users_registered_today": users_registered_today,
        "online_peak": today_online_peak,
    }


@user_route.get("/get_user_status/{tg_id}")
async def get_user_status(tg_id: int, db: AsyncSession = Depends(get_db)):
    """Узнаем, админ пользователь или нет"""

    user = await get_user(db, tg_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_admin:
        return False

    return True


@user_route.get("/test123")
async def test123(db: AsyncSession = Depends(get_db)):
    start_time = datetime.now()
    previous_end = start_time
    total_time_diff = timedelta()
    start = datetime.now()
    get_data = await get_user(db, 1)
    end = datetime.now()
    interval = end - start
    total_time_diff += interval
    logger.info(f'Прошло {interval.seconds} секунд и {interval.microseconds // 1000} миллисекунд на получение юзера1')
    return get_data


@user_route.get("/test1232")
async def test1232():
    start_time = datetime.now()
    previous_end = start_time
    total_time_diff = timedelta()
    start = datetime.now()
    async with sessionmanager.session() as db:
        get_data = await get_user(db, 1)
        end = datetime.now()
        interval = end - start
        total_time_diff += interval
        logger.info(f'Прошло {interval.seconds} секунд и {interval.microseconds // 1000} миллисекунд на получение юзера2')
        return get_data


@user_route.get('/test-perf-123')
async def test_perf(db: CurrentAsyncSession):
    start_time = datetime.now()
    previous_end = start_time
    total_time_diff = timedelta()
    start = datetime.now()
    get_data = await get_user(db, 1)
    end = datetime.now()
    interval = end - start
    total_time_diff += interval
    logger.info(f'Прошло {interval.seconds} секунд и {interval.microseconds // 1000} миллисекунд на получение юзера3')
    return {"time": interval.seconds}