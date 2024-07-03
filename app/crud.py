from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas


async def get_user(db: AsyncSession, tg_id: int):
    result = await db.execute(select(models.User).filter(models.User.tg_id == tg_id))
    return result.scalars().first()


# async def get_user_by_tg_id(db: AsyncSession, tg_id: int):
#     result = await db.execute(select(models.User).filter(models.User.tg_id == tg_id))
#     return result.scalars().first()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_upgrade_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(models.UpgradeCategory).filter(models.UpgradeCategory.id == category_id))
    return result.scalars().first()


async def create_upgrade_category(db: AsyncSession, category: schemas.UpgradeCategoryCreate):
    db_category = models.UpgradeCategory(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def get_upgrade(db: AsyncSession, upgrade_id: int):
    result = await db.execute(select(models.Upgrades).filter(models.Upgrades.id == upgrade_id))
    return result.scalars().first()


async def create_upgrade(db: AsyncSession, upgrade: schemas.UpgradeCreate):
    db_upgrade = models.Upgrades(**upgrade.dict())
    db.add(db_upgrade)
    await db.commit()
    await db.refresh(db_upgrade)
    return db_upgrade


async def create_click(db: AsyncSession, click: schemas.ClickCreate):
    # This function can be expanded to handle click data and associated logic
    pass
