import asyncio
import json
from datetime import datetime, timedelta

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError
from fastapi import APIRouter, Depends, HTTPException, Path, Header
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.user import get_user, create_user, get_user_boost, get_boost_by_id, add_boost, \
    get_boost_by_lvl, get_next_boost, upgrade_user_boost, get_user_bool, get_daily_reward, add_daily_reward
from ..config import loop, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP, KAFKA_TOPIC
from ..cruds.upgrade import get_user_upgrades, get_upgrade_by_id
from ..database import get_db
from ..models import DailyReward
from ..schemas import Message, UserCreate, UserBase, BoostCreateSchema, DailyRewardResponse, CreateDailyRewardSchema, \
    InitDataSchema

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
#             print(f'Consumer msg😍😍😍😍😍😍: {msg}')
#     except Exception as e:
#         print(f"Error consuming messages: {e}")
#     finally:
#         await consumer.stop()


# @user_route.post('/user')
# async def register_send(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     producer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
#     await producer.start()
#
#     try:
#         db_user = await get_user(db, tg_id=user.tg_id)
#         if db_user:
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
#             print(f'Received message: {msg.value.decode("utf-8")}')
#             message = json.loads(msg.value.decode("utf-8"))
#             user_data = UserCreate(**message)
#
#             async with await get_db() as db:
#                 await create_user(db, user_data)
#                 await db.commit()
#     except Exception as e:
#         print(f"Error consuming messages: {e}")
#     finally:
#         await consumer.stop()


@user_route.post('/user')
async def register_send(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, tg_id=user.tg_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    message = {
        "tg_id": user.tg_id,
        "username": user.username,
        "fio": user.fio,
        "invited_tg_id": user.invited_tg_id
    }

    # user_data = UserCreate(**message)
    new_user = await create_user(db, **message)
    if not new_user:
        raise HTTPException(status_code=500, detail="Error")

    return new_user


@user_route.post('/user-login')
async def user_login(user_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current_time = datetime.utcnow()
    last_login = user.last_login or current_time
    time_diff = current_time - last_login

    # Ограничиваем расчет дохода максимум 3 часами
    hours_passed = min(time_diff.total_seconds() / 3600, 3)

    # Получаем все улучшения пользователя
    user_upgrades = await get_user_upgrades(user_id, db)

    # Получаем все апгрейды пользователя асинхронно
    upgrades = await asyncio.gather(
        *[get_upgrade_by_id(db, user_upgrade.upgrade_id) for user_upgrade in user_upgrades]
    )

    # Рассчитываем общий доход в час
    total_hourly_income = sum(
        next((lvl.factor for lvl in upgrade.levels if lvl.lvl == user_upgrade.lvl), 0)
        for user_upgrade, upgrade in zip(user_upgrades, upgrades)
    )

    # Рассчитываем доход за прошедшее время
    total_income = total_hourly_income * hours_passed

    # Обновляем баланс пользователя
    user.money += total_income

    # Обновляем дату последнего входа
    user.last_login = current_time

    # Получаем текущий буст пользователя
    user_boost = await get_user_boost(db, user_id)

    if user_boost:
        boost = await get_boost_by_id(db, user_boost.boost_id)
        if boost:
            boost_data = {
                "boost_id": boost.lvl,
                "name": boost.name,
                "price": boost.price,
                "lvl": boost.lvl,
                "tap_boost": boost.tap_boost,
                "one_tap": boost.one_tap,
                "pillars_10": boost.pillars_10,
                "pillars_30": boost.pillars_30,
                "pillars_100": boost.pillars_100
            }
        else:
            boost_data = {}
    else:
        boost_data = {}
    print('🐟', boost_data)

    await db.commit()
    await db.refresh(user)

    # Преобразуем объект user в словарь
    user_data = UserBase.from_orm(user).dict()
    user_data["total_income"] = total_income
    user_data["boost"] = boost_data

    return user_data


@user_route.post('/logreg')
async def logreg(initData: str = Header(...), db: AsyncSession = Depends(get_db)):
    try:
        # Декодируем строку JSON
        decoded_data = json.loads(initData)

        # Валидируем данные с помощью Pydantic
        # data = InitDataSchema(**decoded_data)
        data = decoded_data
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in header initData")

    tg_id = data.get("id")
    username = data.get("username", "")
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    invited_tg_id = data.get("invited_tg_id", None)

    if not tg_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Пытаемся найти пользователя по tg_id
    db_user = await get_user(db, tg_id)

    if db_user:
        # Пользователь найден, выполняем вход
        current_time = datetime.utcnow()
        last_login = db_user.last_login or current_time
        time_diff = current_time - last_login

        hours_passed = min(time_diff.total_seconds() / 3600, 3)

        user_upgrades = await get_user_upgrades(tg_id, db)
        upgrades = await asyncio.gather(
            *[get_upgrade_by_id(db, user_upgrade.upgrade_id) for user_upgrade in user_upgrades]
        )

        total_hourly_income = sum(
            next((lvl.factor for lvl in upgrade.levels if lvl.lvl == user_upgrade.lvl), 0)
            for user_upgrade, upgrade in zip(user_upgrades, upgrades)
        )

        total_income = total_hourly_income * hours_passed

        db_user.money += total_income
        db_user.last_login = current_time

        user_boost = await get_user_boost(db, tg_id)
        if user_boost:
            boost = await get_boost_by_id(db, user_boost.boost_id)
            boost_data = {
                "boost_id": boost.lvl,
                "name": boost.name,
                "price": boost.price,
                "lvl": boost.lvl,
                "tap_boost": boost.tap_boost,
                "one_tap": boost.one_tap,
                "pillars_10": boost.pillars_10,
                "pillars_30": boost.pillars_30,
                "pillars_100": boost.pillars_100
            } if boost else {}
        else:
            boost_data = {}

        await db.commit()
        await db.refresh(db_user)

        user_data = {
            "tg_id": db_user.tg_id,
            "username": db_user.username,
            "fio": db_user.fio,
            "last_login": db_user.last_login,
            "money": db_user.money,
            "earnings_per_hour": total_hourly_income,
            "total_income": total_income,
            "boost": boost_data
        }

        return user_data
    else:
        # Пользователь не найден, выполняем регистрацию
        new_user = await create_user(
            db,
            tg_id=tg_id,
            username=username,
            fio=first_name,  # Ваша схема использует 'fio', но в данных 'first_name'
            invited_tg_id=invited_tg_id
        )
        if not new_user:
            raise HTTPException(status_code=500, detail="Error creating user")

        boost_data = {
            "boost_id": new_user.boost.lvl,
            "name": new_user.boost.name,
            "price": new_user.boost.price,
            "lvl": new_user.boost.lvl,
            "tap_boost": new_user.boost.tap_boost,
            "one_tap": new_user.boost.one_tap,
            "pillars_10": new_user.boost.pillars_10,
            "pillars_30": new_user.boost.pillars_30,
            "pillars_100": new_user.boost.pillars_100
        } if new_user.boost else {}

        user_data = {
            "tg_id": new_user.user.tg_id,
            "username": new_user.user.username,
            "fio": new_user.user.fio,
            "last_login": new_user.user.last_login,
            "money": new_user.user.money,
            "boost": boost_data
        }
        await db.close()
        return user_data


@user_route.post('/boost')
async def create_upgrade(boost_create: BoostCreateSchema,
                         db: AsyncSession = Depends(get_db)):
    user_data = {
        'name': boost_create.name,
        'lvl': boost_create.lvl,
        "price": boost_create.price,
        'tap_boost': boost_create.tap_boost,
        'one_tap': boost_create.one_tap,
        'pillars_10': boost_create.pillars_10,
        'pillars_30': boost_create.pillars_30,
        'pillars_100': boost_create.pillars_100
    }

    boost = await get_boost_by_lvl(db, boost_lvl=boost_create.lvl)

    if boost:
        raise HTTPException(status_code=409, detail="this lvl is already in use")

    new_boost = await add_boost(db, **user_data)
    if new_boost:
        return new_boost
    else:
        raise HTTPException(status_code=400, detail="failed to create boost")


@user_route.post('/upgrade-boost')
async def upgrade_boost(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_boost = await get_user_boost(db, user_id)

    if not user_boost:
        raise HTTPException(status_code=404, detail="User boost not found")

    # Получаем текущий и следующий уровни буста
    current_boost = await get_boost_by_id(db, user_boost.boost_id)

    if not current_boost:
        # current_boost = await get_boost_by_id(db, 1)
        # if not current_boost:
        raise HTTPException(status_code=404, detail="Current boost not found")

    next_boost = await get_next_boost(db, current_boost.lvl)

    if not next_boost:
        raise HTTPException(status_code=404, detail="Next boost level not found")

    # Проверяем, хватает ли у пользователя денег на покупку следующего уровня
    if user.money < next_boost.price:
        raise HTTPException(status_code=400, detail="Not enough money to upgrade boost")

    # Обновляем уровень буста у пользователя и списываем сумму покупки
    new_user_boost = await upgrade_user_boost(db, user_boost, user, next_boost)

    if not new_user_boost:
        raise HTTPException(status_code=500, detail="failed to improve boost")

    return {
        "user_id": user_boost.user_id,
        "boost_id": user_boost.boost_id,
        "user_money": user.money
    }


@user_route.get("/next-upgrade/{user_id}")
async def get_next_upgrade_func(user_id: int = Path(..., description="user id"),
                                  db: AsyncSession = Depends(get_db)) -> BoostCreateSchema:
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_boost = await get_user_boost(db, user_id)

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


@user_route.post('/claim-daily-reward', response_model=DailyRewardResponse)
async def claim_daily_reward(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current_time = datetime.utcnow()
    received_last_daily_reward = user.received_last_daily_reward or current_time

    # Проверка, прошло ли более одного дня с последнего входа
    if current_time > received_last_daily_reward + timedelta(days=2):
        user.days_in_row = 0

    # Проверка, прошло ли менее одного дня с последнего входа
    if current_time < received_last_daily_reward + timedelta(days=1):
        raise HTTPException(status_code=404, detail="less than one day has passed")

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

    await db.commit()
    await db.refresh(user)

    return DailyRewardResponse(
        day=daily_reward.day,
        reward=daily_reward.reward,
        total_money=user.money
    )


@user_route.post('/create-daily-reward')
async def create_daily_reward(daily_reward: CreateDailyRewardSchema,
                              db: AsyncSession = Depends(get_db)):
    user_data = {
        'day': daily_reward.day,
        'reward': daily_reward.reward,
    }

    old_daily_reward = await get_daily_reward(db, day=daily_reward.day)

    if old_daily_reward:
        raise HTTPException(status_code=409, detail="this day is already in use")

    new_daily_reward = await add_daily_reward(db, **user_data)
    if new_daily_reward:
        return new_daily_reward
    else:
        raise HTTPException(status_code=400, detail="failed to create boost")

