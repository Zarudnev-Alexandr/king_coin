from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas, crud, kafka_producer
from .database import get_db

app = FastAPI()

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, tg_id=user.tg_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await crud.create_user(db=db, user=user)

@app.post("/clicks/", response_model=schemas.Click)
async def create_click(click: schemas.ClickCreate, db: AsyncSession = Depends(get_db)):
    await kafka_producer.send_click_event(click.user_id)
    return await crud.create_click(db=db, click=click)
