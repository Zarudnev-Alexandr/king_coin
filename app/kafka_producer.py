from aiokafka import AIOKafkaProducer
import asyncio
import os

KAFKA_SERVER = 'kafka:9092'


# async def send_click_event(user_id: int):
#     producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)
#     await producer.start()
#     try:
#         message = f"User {user_id} clicked".encode('utf-8')
#         await producer.send_and_wait("clicks_topic", message)
#     finally:
#         await producer.stop()


async def send_register_user_event(user_data: dict):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)
    await producer.start()
    try:
        message = f"Register {user_data}".encode('utf-8')
        await producer.send_and_wait("register_topic", message)
        print(f"😍Sent message: {message}")
    except Exception as e:
        print(f"Producer error: {e}")
    finally:
        await producer.stop()
