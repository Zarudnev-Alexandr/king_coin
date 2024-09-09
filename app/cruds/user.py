import datetime
from datetime import date

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas
from app.models import UserBoost, Boost, DailyReward, Level


async def get_user(db: AsyncSession, tg_id: int):
    result = await db.execute(select(models.User).filter(models.User.tg_id == tg_id))
    return result.scalars().first()


async def get_user_bool(db: AsyncSession, tg_id: int):
    result = await db.execute(select(models.User).filter(models.User.tg_id == tg_id))
    if result.scalars().first():
        return True
    else:
        return False


async def create_user(db: AsyncSession, **kwargs):
    user_data = kwargs
    user_data['last_login'] = datetime.datetime.now()
    user_data['received_last_daily_reward'] = datetime.datetime.now() - datetime.timedelta(days=1)

    # Создаем пользователя
    user = models.User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Создаем объект UserBoost для нового пользователя
    user_boost_data = {
        "user_id": user.tg_id,
        "boost_id": 0
    }
    user_boost = UserBoost(**user_boost_data)
    db.add(user_boost)
    await db.commit()
    await db.refresh(user_boost)

    return user_boost


async def get_user_boost(db: AsyncSession, user_id: int):
    user_boosts = await db.execute(select(UserBoost).where(UserBoost.user_id == user_id))
    user_boost = user_boosts.scalars().first()
    return user_boost


async def get_boost_by_id(db: AsyncSession, boost_id: int):
    boost = await db.execute(select(Boost).where(Boost.lvl == boost_id))
    boost = boost.scalars().first()
    return boost


async def get_boost_by_lvl(db: AsyncSession, boost_lvl: int):
    """Буст по уровню"""
    result = await db.execute(select(Boost).filter(Boost.lvl == boost_lvl))
    return result.scalars().first()


async def update_user_level(db: AsyncSession, user):
    """Апгрейд уровня пользователя"""
    levels = await db.execute(select(Level).order_by(Level.lvl))
    levels = levels.unique().scalars().all()

    new_level = user.lvl
    next_level = None
    new_taps_for_level = user.taps_for_level

    for level in levels:
        # Обновляем текущий уровень, если его можно достичь и он выше текущего
        if user.money >= level.required_money and level.lvl > new_level:

            new_level = level.lvl
            new_taps_for_level = level.taps_for_level

        # Определяем следующий уровень, который будет следующим после текущего уровня пользователя
        if level.lvl > new_level:
            next_level = level
            break

    # Обновить уровень пользователя, если он увеличился
    if user.lvl != new_level:
        user.lvl = new_level
        user.taps_for_level = new_taps_for_level
        await db.commit()
        await db.refresh(user)

    if new_level == 1:
        user.taps_for_level = 2
        await db.commit()
        await db.refresh(user)

    return next_level


async def get_next_boost(db: AsyncSession, current_lvl: int):
    next_boost = await db.execute(select(Boost).where(Boost.lvl == current_lvl + 1))
    next_boost = next_boost.scalars().first()
    # if next_boost:
    #     await db.refresh(next_boost)  # Обновляем объект из базы данных
    return next_boost


async def add_boost(db: AsyncSession, **kwargs) -> Boost:
    """Создание буста"""
    boost_data = kwargs

    boost = Boost(**boost_data)
    db.add(boost)
    await db.commit()
    return boost


async def upgrade_user_boost(db, user_boost, user, next_boost):
    user_boost.boost_id = next_boost.lvl
    user.money -= next_boost.price

    await db.commit()
    await db.refresh(user_boost)
    return user_boost


async def get_daily_reward(db: AsyncSession, day: int) -> DailyReward:
    result = await db.execute(select(DailyReward).where(DailyReward.day == day))
    return result.scalars().first()


async def get_daily_reward_all(db: AsyncSession):
    result = await db.execute(
        select(DailyReward)
    )
    return result.unique().scalars().all()


async def add_daily_reward(db: AsyncSession, **kwargs) -> DailyReward:
    """Создание ежедневной награды"""
    daily_reward_data = kwargs

    daily_reward = DailyReward(**daily_reward_data)
    db.add(daily_reward)
    await db.commit()
    return daily_reward


async def get_count_of_all_users(db: AsyncSession):
    """Считаем количество всех пользователей в бд"""

    result = await db.execute(
        select(func.count(models.User.tg_id))
    )
    count_of_all_users = result.scalar_one()

    return count_of_all_users


async def get_all_earned_money(db: AsyncSession):
    """Считаем количество всех заработанных денег в бд"""

    result = await db.execute(
        select(func.sum(models.User.money))
    )
    count_of_all_users = result.scalar_one()

    return count_of_all_users


async def get_users_registered_today(db: AsyncSession):
    """Считаем количество пользователей, зарегистрировавшихся сегодня"""

    today = datetime.datetime.utcnow()

    result = await db.scalar(
        select(func.count(models.User.tg_id)).filter(
            func.date(models.User.created) == today.date()
        )
    )

    print("😀😀😀", result)

    return result

