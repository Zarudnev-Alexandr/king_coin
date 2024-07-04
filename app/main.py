import asyncio

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, crud, kafka_producer, kafka_consumer, routers
from .database import get_db
from .routers import user

app = FastAPI()


# @app.post("/users/", response_model=schemas.User)
# async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
#     db_user = await crud.get_user(db, tg_id=user.tg_id)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     await kafka_producer.send_register_user_event(user.dict())
#     return user  # Возвращаем созданного пользователя, потому что реальное создание будет асинхронным через Kafka


# @app.post("/clicks/", response_model=schemas.Click)
# async def create_click(click: schemas.ClickCreate, db: AsyncSession = Depends(get_db)):
#     await kafka_producer.send_click_event(click.user_id)
#     return await crud.create_click(db=db, click=click)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(kafka_consumer.consume_register())

app.include_router(user.user_route)
asyncio.create_task(user.consume())
