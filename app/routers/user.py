from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException
# from schema import Message
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import loop, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP, KAFKA_TOPIC
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json

from ..crud import get_user, create_user
from ..database import get_db
from ..schemas import Message, UserCreate

user_route = APIRouter()


@user_route.post('/create_message')
async def send(message: Message):
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        print(f'Sendding message with value: {message}')
        value_json = json.dumps(message.__dict__).encode('utf-8')
        await producer.send_and_wait(topic=KAFKA_TOPIC, value=value_json)
    finally:
        await producer.stop()


async def consume():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id=KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            print(f'Consumer msg: {msg}')
    finally:
        await consumer.stop()


@user_route.post('/user')
async def register_func(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Подключаемся к Kafka для отправки сообщений
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()

    try:
        db_user = await get_user(db, tg_id=user.tg_id)
        if db_user:
            raise HTTPException(status_code=400, detail="User already registered")

        created_user = await create_user(db, user)

        message = {
            "event": "user_registered",
            "tg_id": created_user.tg_id,
            "username": created_user.username,
            "fio": created_user.fio,
            "invited_tg_id": created_user.invited_tg_id
        }
        value_json = json.dumps(message).encode('utf-8')
        await producer.send_and_wait(topic=KAFKA_TOPIC, value=value_json)

        return created_user

    finally:
        await producer.stop()



