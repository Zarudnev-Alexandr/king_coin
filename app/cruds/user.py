from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas
from app.models import UserBoost, Boost, DailyReward


async def get_user(db: AsyncSession, tg_id: int):
    result = await db.execute(select(models.User).filter(models.User.tg_id == tg_id))
    return result.scalars().first()


async def get_user_bool(db: AsyncSession, tg_id: int):
    result = await db.execute(select(models.User).filter(models.User.tg_id == tg_id))
    if result.scalars().first():
        return True
    else:
        return False


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db_user.last_login=date.today()
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


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


async def get_next_boost(db: AsyncSession, current_lvl: int):
    next_boost = await db.execute(select(Boost).where(Boost.lvl == current_lvl + 1))
    next_boost = next_boost.scalars().first()
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
    return user_boost


async def get_daily_reward(db: AsyncSession, day: int) -> DailyReward:
    result = await db.execute(select(DailyReward).where(DailyReward.day == day))
    return result.scalars().first()


async def add_daily_reward(db: AsyncSession, **kwargs) -> DailyReward:
    """Создание ежедневной награды"""
    daily_reward_data = kwargs

    daily_reward = DailyReward(**daily_reward_data)
    db.add(daily_reward)
    await db.commit()
    return daily_reward


# async def get_upgrade_category(db: AsyncSession, category_id: int):
#     result = await db.execute(select(models.UpgradeCategory).filter(models.UpgradeCategory.id == category_id))
#     return result.scalars().first()


# async def create_upgrade_category(db: AsyncSession, category: schemas.UpgradeCategoryCreate):
#     db_category = models.UpgradeCategory(**category.dict())
#     db.add(db_category)
#     await db.commit()
#     await db.refresh(db_category)
#     return db_category
#
#
# async def get_upgrade(db: AsyncSession, upgrade_id: int):
#     result = await db.execute(select(models.Upgrades).filter(models.Upgrades.id == upgrade_id))
#     return result.scalars().first()
#
#
# async def create_upgrade(db: AsyncSession, upgrade: schemas.UpgradeCreate):
#     db_upgrade = models.Upgrades(**upgrade.dict())
#     db.add(db_upgrade)
#     await db.commit()
#     await db.refresh(db_upgrade)
#     return db_upgrade
#
#
# async def create_click(db: AsyncSession, click: schemas.ClickCreate):
#     # This function can be expanded to handle click data and associated logic
#     pass
