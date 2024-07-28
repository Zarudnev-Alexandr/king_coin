from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .database import sessionmanager
from .routers import task
from .routers import upgrade
from .routers import user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или укажите конкретные домены, если нужно
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.user_route, prefix='/api/users', tags=['Users'])
app.include_router(upgrade.upgrade_route, prefix='/api/upgrades', tags=['Upgrades'])
app.include_router(task.task_route, prefix='/api/tasks', tags=['Tasks'])


@app.on_event("startup")
async def on_startup():
    sessionmanager.init_db()

# @app.on_event("startup")
# async def on_startup():
#     global async_session
#     async_session = await init_db()

# @app.on_event("startup")
# async def startup_event():
    # asyncio.create_task(user.consume())
    # asyncio.create_task(user.consume_register())


