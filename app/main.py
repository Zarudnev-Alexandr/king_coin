import asyncio

from fastapi import FastAPI

from .routers import user
from .routers import upgrade

app = FastAPI()

app.include_router(user.user_route, prefix='/api/users', tags=['Users'])
app.include_router(upgrade.upgrade_route, prefix='/api/upgrades', tags=['Upgrades'])


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(user.consume())
    asyncio.create_task(user.consume_register())


