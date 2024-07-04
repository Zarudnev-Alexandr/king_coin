from aiokafka import AIOKafkaConsumer
import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession
from .database import async_session
from . import crud, schemas

KAFKA_SERVER = 'kafka:9092'


# async def consume_clicks():
#     consumer = AIOKafkaConsumer(
#         'clicks_topic',
#         bootstrap_servers=KAFKA_SERVER,
#         group_id="clicks_group"
#     )
#     await consumer.start()
#     try:
#         async for message in consumer:
#             click_info = message.value.decode('utf-8')
#             user_id = int(click_info.split(" ")[1])
#             async with async_session() as db:
#                 await crud.create_click(db, schemas.ClickCreate(user_id=user_id))
#             print(f"Processed click for user {user_id}")
#     finally:
#         await consumer.stop()


async def consume_register():
    consumer = AIOKafkaConsumer(
        'register_topic',
        bootstrap_servers=KAFKA_SERVER,
        group_id="register_group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            try:
                register_info = message.value.decode('utf-8')
                print(f"😛Received message: {register_info}")
                user_data = eval(register_info.split(" ", 1)[1])  # Преобразуем строку обратно в словарь
                user_create = schemas.UserCreate(**user_data)
                async with async_session() as db:
                    await crud.create_user(db, user=user_create)
                print(f"Processed registration for user {user_data}")
            except Exception as e:
                print(f"Error processing message: {e}")
    except Exception as e:
        print(f"Consumer error: {e}")
    finally:
        await consumer.stop()

# Для тестирования в изоляции
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume_register())