import asyncio
import json
from datetime import datetime

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.user import get_user, create_user
from ..config import loop, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP, KAFKA_TOPIC
from ..cruds.upgrade import get_user_upgrades, get_upgrade_by_id
from ..database import get_db
from ..schemas import Message, UserCreate, UserBase

user_route = APIRouter()


@user_route.post('/create_message')
async def send(message: Message):
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        value_json = json.dumps(message.__dict__).encode('utf-8')
        await producer.send_and_wait(topic=KAFKA_TOPIC, value=value_json)
    finally:
        await producer.stop()


async def consume():
    try:
        consumer = AIOKafkaConsumer(KAFKA_TOPIC,
                                    loop=loop,
                                    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                    group_id=KAFKA_CONSUMER_GROUP)
    except KafkaError as err:
        raise Exception(f"🥰🥰🥰{err}")

    await consumer.start()
    try:

        async for msg in consumer:
            print(f'Consumer msg😍😍😍😍😍😍: {msg}')
    except Exception as e:
        print(f"Error consuming messages: {e}")
    finally:
        await consumer.stop()


@user_route.post('/user')
async def register_send(user: UserCreate, db: AsyncSession = Depends(get_db)):
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()

    try:
        db_user = await get_user(db, tg_id=user.tg_id)
        if db_user:
            raise HTTPException(status_code=400, detail="User already registered")

        # Собираем сообщение для Kafka
        message = {
            "tg_id": user.tg_id,
            "username": user.username,
            "fio": user.fio,
            "invited_tg_id": user.invited_tg_id
        }
        value_json = json.dumps(message).encode('utf-8')
        await producer.send_and_wait(topic="user_registration", value=value_json)

        return {"status": "User registration message sent to Kafka"}

    finally:
        await producer.stop()


async def consume_register():
    consumer = AIOKafkaConsumer(
        "user_registration",
        loop=loop,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="registration_group"
    )

    await consumer.start()
    try:
        async for msg in consumer:
            print(f'Received message: {msg.value.decode("utf-8")}')
            message = json.loads(msg.value.decode("utf-8"))
            user_data = UserCreate(**message)

            async with await get_db() as db:
                await create_user(db, user_data)
                await db.commit()
    except Exception as e:
        print(f"Error consuming messages: {e}")
    finally:
        await consumer.stop()


@user_route.post('/user-login')
async def user_login(user_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current_time = datetime.utcnow()
    last_login = user.last_login_date or current_time
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
    user.last_login_date = current_time

    await db.commit()
    await db.refresh(user)

    # Преобразуем объект user в словарь
    user_data = UserBase.from_orm(user).dict()
    user_data["total_income"] = total_income

    return user_data
