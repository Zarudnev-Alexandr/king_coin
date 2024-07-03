from aiokafka import AIOKafkaProducer
import asyncio
import os

KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'localhost:9092')


async def send_click_event(user_id: int):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)
    await producer.start()
    try:
        message = f"User {user_id} clicked".encode('utf-8')
        await producer.send_and_wait("clicks_topic", message)
    finally:
        await producer.stop()
