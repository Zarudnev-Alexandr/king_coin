from datetime import datetime

import requests
from environs import Env
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task, UserTask, User

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')


async def add_task(db: AsyncSession, **kwargs) -> Task:
    """Создание задания"""
    task_data = kwargs

    task = Task(**task_data)
    db.add(task)
    await db.commit()
    return task


async def get_task(db: AsyncSession, task_id: int):
    """Получаем задание по id"""
    result = await db.execute(select(Task).filter(Task.id == task_id))
    return result.scalars().first()


async def get_user_task(db: AsyncSession, task_id: int, user_id: int):
    """Получаем отношение пользователя к конкретному заданию"""
    result = await db.execute(select(UserTask).filter(UserTask.user_id == user_id, UserTask.task_id == task_id))
    return result.scalars().first()


async def create_user_task(db: AsyncSession, task_id: int, user_id: int):
    """Создаем отношение пользователь - задание"""
    new_user_task = UserTask(user_id=user_id, task_id=task_id, completed=False)
    db.add(new_user_task)
    await db.commit()
    return new_user_task


async def get_invited_count(db: AsyncSession, user_id: int) -> int:
    """Получаем, скольких человек пригласил пользователь"""
    result = await db.execute(
        select(func.count(User.tg_id)).where(User.invited_tg_id == user_id)
    )
    invited_count = result.scalar_one()
    return invited_count


async def complete_user_task(db: AsyncSession, user: User, task: Task, user_task: UserTask = None):
    """Помечаем задание как выполненное у этого пользователя"""
    if not user_task:
        user_task = await create_user_task(db, task.id, user.tg_id)

    await db.refresh(user)
    await db.refresh(task)

    user.money += task.reward
    user_task.completed = True
    user_task.completion_date = func.now()
    await db.commit()


def check_telegram_subscription(chat_id: int, user_id: int) -> bool:
    """Проверяем, подписан ли пользователь на тг канал или нет"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
    params = {
        "chat_id": chat_id,
        "user_id": user_id
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['ok'] and data['result']['status'] in ['member', 'administrator', 'creator']:
        return True
    return False


async def get_all_tasks(db: AsyncSession):
    """Получаем все задания"""
    current_time = datetime.utcnow()
    result = await db.execute(
        select(Task).where(
            or_(Task.end_time.is_(None), Task.end_time >= current_time)
        )
    )
    tasks = result.unique().scalars().all()
    return tasks



async def get_user_tasks(db: AsyncSession, user_id: int):
    """Получаем все задания, связанные с пользователем"""
    result = await db.execute(select(UserTask).filter(UserTask.user_id == user_id))
    return result.unique().scalars().all()