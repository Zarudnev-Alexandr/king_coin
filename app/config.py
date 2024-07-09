import asyncio

# env Variable
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = "kafkazxc123"
KAFKA_CONSUMER_GROUP = "groupZXC"
loop = asyncio.get_event_loop()
