from datetime import datetime, timedelta
import json

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.added_funcs import decode_init_data
from app.cruds.task import add_task, get_task, get_user_task, get_invited_count, create_user_task, complete_user_task, \
    check_telegram_subscription, get_all_tasks, get_user_tasks
from app.cruds.user import get_user
from app.database import get_db
from app.models import TaskType
from app.schemas import TaskCreateSchema, TaskBaseSchema, TaskResponseSchema

task_route = APIRouter()


@task_route.post("/", response_model=TaskBaseSchema)
async def create_task(task: TaskCreateSchema, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, tg_id=task.user_creator_id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="You have no permission to create task")

    end_time = None
    if task.days_active is not None:
        end_time = datetime.utcnow() + timedelta(days=task.days_active)

    task_data = {
        "name": task.name,
        "description": task.description,
        "type": task.type,
        "reward": task.reward,
        "requirement": task.requirement,
        "link": task.link,
        "end_time": end_time
    }

    new_task = await add_task(db, **task_data)
    if new_task:
        return new_task
    else:
        raise HTTPException(status_code=400, detail="Failed to create task")


@task_route.post("/check/{task_id}")
async def check_task_completion(task_id: int, initData: str = Header(...), db: AsyncSession = Depends(get_db)):
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.end_time and task.end_time < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Task timed out")

    user_task = await get_user_task(db, task_id, user.tg_id)
    if user_task and user_task.completed:
        raise HTTPException(status_code=400, detail="Task already completed")

    # Если задание на приглашение пользователей
    if task.type == TaskType.INVITE:
        invited_count = await get_invited_count(db, user.tg_id)
        if invited_count < task.requirement:
            if not user_task:
                await create_user_task(db, task_id, user.tg_id)
            raise HTTPException(status_code=400,
                                detail="The task was not completed, the number of invited users is not enough")

        if not user_task:
            user_task = await create_user_task(db, task_id, user.tg_id)
        await complete_user_task(db, user, task, user_task)

    # Если задание - это подписаться на тг канал
    elif task.type == TaskType.SUBSCRIBE_TELEGRAM:
        is_subscribed = check_telegram_subscription(task.requirement, user.tg_id)
        if not is_subscribed:
            if not user_task:
                await create_user_task(db, task_id, user.tg_id)
            raise HTTPException(status_code=400,
                                detail="The task was not completed, the user is not subscribed to the channel")

        if not user_task:
            user_task = await create_user_task(db, task_id, user.tg_id)
        await complete_user_task(db, user, task, user_task)

    # Если это задание без проверки
    elif task.type == TaskType.GENERIC:
        if not user_task:
            user_task = await create_user_task(db, task_id, user.tg_id)
        await complete_user_task(db, user, task, user_task)

    await db.refresh(user)
    return {"status": "Task checked and updated",
            "money_received": task.reward,
            "current_user_money": user.money}


@task_route.get("/tasks", response_model=list[TaskResponseSchema])
async def get_tasks_for_user(initData: str = Header(...), db: AsyncSession = Depends(get_db)):
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    tasks = await get_all_tasks(db)
    user_tasks = await get_user_tasks(db, user.tg_id)

    user_task_ids = {ut.task_id: ut.completed for ut in user_tasks}

    tasks_with_completion_flag = []
    for task in tasks:
        task_dict = task.to_dict()
        task_dict['temporary_task'] = True if task.end_time is not None else False
        task_dict['completed'] = user_task_ids.get(task.id, False)
        tasks_with_completion_flag.append(task_dict)

    return tasks_with_completion_flag
