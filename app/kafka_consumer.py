from aiokafka import AIOKafkaConsumer
import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession
from .database import async_session
from . import crud, schemas

KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'localhost:9092')

async def consume_clicks():
    consumer = AIOKafkaConsumer(
        'clicks_topic',
        bootstrap_servers=KAFKA_SERVER,
        group_id="clicks_group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            click_info = message.value.decode('utf-8')
            user_id = int(click_info.split(" ")[1])
            async with async_session() as db:
                await crud.create_click(db, schemas.ClickCreate(user_id=user_id))
            print(f"Processed click for user {user_id}")
    finally:
        await consumer.stop()

loop = asyncio.get_event_loop()
loop.run_until_complete(consume_clicks())
