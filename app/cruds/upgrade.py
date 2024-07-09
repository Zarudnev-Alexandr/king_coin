from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UpgradeCategory, Upgrades, UpgradeLevel, UserUpgrades


async def get_upgrade_category_by_id(db: AsyncSession, upgrade_category_id: int):
    """Категория улучшений (карточек) по id"""
    upgrade_category = await db.get(UpgradeCategory, upgrade_category_id)
    return upgrade_category


async def get_upgrade_category_by_name(db: AsyncSession, upgrade_category_name: str):
    """Категория улучшений (карточек) по названию"""
    result = await db.execute(select(UpgradeCategory).filter(UpgradeCategory.category == upgrade_category_name))
    return result.scalars().first()


async def get_all_upgrade_category(db: AsyncSession):
    """Все категории улучшений (карточкек)"""
    query = select(UpgradeCategory)

    result = await db.execute(query)
    upgrades = result.scalars().all()
    return upgrades


async def create_upgrade_category(db: AsyncSession, **kwargs) -> UpgradeCategory:
    """Создание категории улучшений (карточек)"""
    user_data = kwargs

    upgrade_category = UpgradeCategory(**user_data)
    db.add(upgrade_category)
    await db.commit()
    return upgrade_category


async def get_upgrade_by_id(db: AsyncSession, upgrade_id: int):
    """Улучшение (карточка) по id"""
    upgrade = await db.get(Upgrades, upgrade_id)
    return upgrade


async def get_upgrade_by_name(db: AsyncSession, upgrade_name: str):
    """Улучшение (карточка) по названию"""
    result = await db.execute(select(Upgrades).filter(Upgrades.name == upgrade_name))
    return result.scalars().first()


async def get_all_upgrades_in_shop(category_id: int, db: AsyncSession):
    """Все улучшения (карточки) в магазине"""
    query = select(Upgrades).where(Upgrades.is_in_shop == True)
    if category_id is not None:
        query = query.where(Upgrades.category_id == category_id)

    result = await db.execute(query)
    upgrades = result.scalars().all()
    return upgrades


async def get_all_upgrades(category_id: int, db: AsyncSession):
    """Все улучшения (карточки)"""
    query = select(Upgrades)
    if category_id is not None:
        query = query.where(Upgrades.category_id == category_id)

    result = await db.execute(query)
    upgrades = result.scalars().all()
    return upgrades


async def add_upgrade(db: AsyncSession, **kwargs) -> Upgrades:
    """Создание улучшения (карточки)"""
    user_data = kwargs

    upgrade = Upgrades(**user_data)
    db.add(upgrade)
    await db.commit()
    return upgrade


async def get_upgrade_level(upgrade_id: int, lvl: int, db: AsyncSession):
    """Получаем уровень улучшения"""

    result = await db.execute(select(UpgradeLevel)
                              .filter(UpgradeLevel.upgrade_id == upgrade_id)
                              .filter(UpgradeLevel.lvl == lvl))
    return result.scalars().first()


async def add_upgrade_level(db: AsyncSession, **kwargs) -> UpgradeLevel:
    """Создание уровня улучшения (карточки)"""
    user_data = kwargs

    upgrade_level = UpgradeLevel(**user_data)
    db.add(upgrade_level)
    await db.commit()
    return upgrade_level


async def get_user_upgrades_by_upgrade_id(user_id: int, upgrade_id: int, db: AsyncSession):
    """Получаем все покупки пользователя по определенному улучшению"""

    result = await db.execute(select(UserUpgrades)
                              .filter(UserUpgrades.user_id == user_id)
                              .filter(UserUpgrades.upgrade_id == upgrade_id)
                              .filter(UpgradeLevel.upgrade_id == upgrade_id))
    return result.scalars().first()


async def add_bought_upgrade(db, user_id: int, upgrade_id: int, lvl: int) -> UserUpgrades:
    """Adds a new upgrade record for the user"""
    user_upgrade = UserUpgrades(user_id=user_id, upgrade_id=upgrade_id, lvl=lvl)
    db.add(user_upgrade)
    await db.commit()
    await db.refresh(user_upgrade)
    return user_upgrade


async def process_upgrade(user, user_upgrade, upgrade, db):
    """Process the upgrade, incrementing levels as long as user has enough money"""
    next_lvl = user_upgrade.lvl + 1
    next_lvl_data = next((lvl for lvl in upgrade.levels if lvl.lvl == next_lvl), None)

    if not next_lvl_data:
        raise HTTPException(status_code=400, detail="Level is max!")

    if user.money < next_lvl_data.price:
        raise HTTPException(status_code=400, detail="You have not money to upgrade")

    user.money -= next_lvl_data.price
    user_upgrade.lvl += 1
    await db.commit()

    await db.refresh(user)
    await db.refresh(user_upgrade)


async def get_user_upgrades(user_id: int, db: AsyncSession) -> List[UserUpgrades]:
    result = await db.execute(
        select(UserUpgrades).where(UserUpgrades.user_id == user_id)
    )
    return result.scalars().all()


async def get_user_upgrades_in_this_category(user_id: int, category_id: int, db: AsyncSession) -> List[UserUpgrades]:
    result = await db.execute(
        select(UserUpgrades).\
        join(Upgrades).join(UpgradeCategory).\
        filter(UserUpgrades.user_id == user_id, UpgradeCategory.id == category_id)
    )
    return result.scalars().all()
