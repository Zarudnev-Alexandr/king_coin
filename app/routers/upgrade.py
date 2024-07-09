from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.upgrade import get_upgrade_category_by_name, create_upgrade_category, get_upgrade_category_by_id, \
    get_upgrade_by_name, add_upgrade, get_upgrade_by_id, get_all_upgrades_in_shop, get_all_upgrades, \
    get_all_upgrade_category, get_upgrade_level, add_upgrade_level, get_user_upgrades_by_upgrade_id, add_bought_upgrade, \
    process_upgrade, get_user_upgrades_in_this_category
from app.cruds.user import get_user, get_user_bool
from app.database import get_db
from app.models import UpgradeLevel
from app.schemas import UpgradeCategoryCreateSchema, UpgradeCategorySchema, CreateUpgradeSchema, UpgradeSchema, \
    UpgradeLevelSchema, UpgradeWithLevelsSchema, UserUpgradeCreateSchema, UserUpgradeSchema

upgrade_route = APIRouter()


@upgrade_route.post('/upgrade-category')
async def create_upgrade_category_func(upgrade_category_create: UpgradeCategoryCreateSchema,
                                       db: AsyncSession = Depends(get_db)) -> UpgradeCategorySchema:
    user_data = {
        "category": upgrade_category_create.category
    }
    upgrade_category = await get_upgrade_category_by_name(db, upgrade_category_name=upgrade_category_create.category)

    if upgrade_category:
        raise HTTPException(status_code=409, detail="this name is already in use")

    new_upgrade_category = await create_upgrade_category(db, **user_data)
    if new_upgrade_category:
        return new_upgrade_category
    else:
        raise HTTPException(status_code=400, detail="failed to create upgrade category")


@upgrade_route.get('/upgrade-category/all')
async def get_upgrade_category_all(db: AsyncSession = Depends(get_db)) -> list[UpgradeCategorySchema]:
    upgrade_categories = await get_all_upgrade_category(db)

    if not upgrade_categories:
        raise HTTPException(status_code=404, detail="upgrades categories not found")
    return upgrade_categories


@upgrade_route.get('/upgrade-category/{identifier}/{user_id}')
async def get_upgrade_category(identifier: str = Path(..., description="Upgrade category id or name"),
                               user_id: int = Path(..., description="user id"),
                               db: AsyncSession = Depends(get_db)) -> UpgradeCategorySchema:

    user = await get_user_bool(db=db, tg_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if identifier.isdigit():
        upgrade_category = await get_upgrade_category_by_id(db, upgrade_category_id=int(identifier))
    else:
        upgrade_category = await get_upgrade_category_by_name(db, upgrade_category_name=identifier)

    if not upgrade_category:
        raise HTTPException(status_code=404, detail="Upgrade category not found")

    user_upgrades_in_this_category = await get_user_upgrades_in_this_category(user_id, upgrade_category.id, db)

    user_upgrades_dict = {upgrade.upgrade_id: upgrade for upgrade in user_upgrades_in_this_category}

    filtered_upgrades = []
    for upgrade in upgrade_category.upgrades:
        if not upgrade.is_in_shop:
            continue

        current_level = user_upgrades_dict.get(upgrade.id, None)
        if current_level:
            upgrade.lvl = current_level.lvl
            upgrade.is_bought = True
        else:
            upgrade.lvl = 0
            upgrade.is_bought = False

        next_upgrade_level = await db.execute(
            select(UpgradeLevel).filter_by(upgrade_id=upgrade.id, lvl=upgrade.lvl + 1)
        )
        next_upgrade_level = next_upgrade_level.scalars().first()

        current_upgrade_level = await db.execute(
            select(UpgradeLevel).filter_by(upgrade_id=upgrade.id, lvl=upgrade.lvl)
        )
        current_upgrade_level = current_upgrade_level.scalars().first()
        upgrade.factor = next_upgrade_level.factor if next_upgrade_level else current_upgrade_level.factor

        upgrade.price_of_next_lvl = next_upgrade_level.price if next_upgrade_level else None

        filtered_upgrades.append(upgrade)

    upgrade_category.upgrades = filtered_upgrades

    return upgrade_category



@upgrade_route.post('/upgrade')
async def create_upgrade(upgrade_create: CreateUpgradeSchema,
                         db: AsyncSession = Depends(get_db)) -> UpgradeSchema:
    user_data = {
        "name": upgrade_create.name,
        "category_id": upgrade_create.category_id,
        "image_url": upgrade_create.image_url,
        "is_in_shop": upgrade_create.is_in_shop
    }

    upgrade = await get_upgrade_by_name(db, upgrade_name=upgrade_create.name)

    if upgrade:
        raise HTTPException(status_code=409, detail="this name is already in use")

    new_upgrade = await add_upgrade(db, **user_data)
    if new_upgrade:
        return new_upgrade
    else:
        raise HTTPException(status_code=400, detail="failed to create upgrade")


@upgrade_route.get('/upgrade/all')
async def get_upgrade_category_all(category_id: int = Query(default=None),
                                   is_in_shop: bool = Query(default=False),
                                   db: AsyncSession = Depends(get_db)) -> list[UpgradeSchema]:
    if is_in_shop:
        upgrades = await get_all_upgrades_in_shop(category_id, db)
    else:
        upgrades = await get_all_upgrades(category_id, db)

    if not upgrades:
        raise HTTPException(status_code=404, detail="upgrades not found")
    return upgrades


@upgrade_route.get('/upgrade/{identifier}')
async def get_upgrade_category(identifier: str = Path(..., description="Upgrade id or name"),
                               db: AsyncSession = Depends(get_db)) -> UpgradeWithLevelsSchema:
    if identifier.isdigit():
        upgrade = await get_upgrade_by_id(db, upgrade_id=int(identifier))
    else:
        upgrade = await get_upgrade_by_name(db, upgrade_name=identifier)

    if upgrade:
        return upgrade
    else:
        raise HTTPException(status_code=404, detail="Upgrade not found")


@upgrade_route.post('/upgrade-level')
async def create_upgrade(upgrade_level_create: UpgradeLevelSchema,
                         db: AsyncSession = Depends(get_db)) -> UpgradeLevelSchema:
    user_data = {
        "upgrade_id": upgrade_level_create.upgrade_id,
        "lvl": upgrade_level_create.lvl,
        "factor": upgrade_level_create.factor,
        "price": upgrade_level_create.price
    }

    if upgrade_level_create.lvl < 1:
        raise HTTPException(status_code=400, detail="level cannot be less than 1")

    upgrade = await get_upgrade_by_id(db, upgrade_id=upgrade_level_create.upgrade_id)

    if not upgrade:
        raise HTTPException(status_code=404, detail="upgrade not found")

    upgrade_level = await get_upgrade_level(upgrade_level_create.upgrade_id, upgrade_level_create.lvl, db)

    if upgrade_level:
        raise HTTPException(status_code=409, detail="this upgrade level is already in use")

    new_upgrade_level = await add_upgrade_level(db, **user_data)
    if new_upgrade_level:
        return new_upgrade_level
    else:
        raise HTTPException(status_code=400, detail="failed to create upgrade level")


@upgrade_route.post('/buy-upgrade')
async def buy_upgrade(user_upgrade_create: UserUpgradeCreateSchema,
                      db: AsyncSession = Depends(get_db)) -> UserUpgradeSchema:
    user_id = user_upgrade_create.user_id
    upgrade_id = user_upgrade_create.upgrade_id

    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    upgrade = await get_upgrade_by_id(db, upgrade_id)
    if not upgrade:
        raise HTTPException(status_code=404, detail="Upgrade not found")

    if not upgrade.is_in_shop:
        raise HTTPException(status_code=404, detail="Upgrade not in shop")

    if len(upgrade.levels) < 1:
        raise HTTPException(status_code=404, detail="list of levels is empty")

    user_upgrade = await get_user_upgrades_by_upgrade_id(user_id, upgrade_id, db)
    print('😂😂😂😂😂😂', user_upgrade)

    if not user_upgrade:
        user_upgrade = await add_bought_upgrade(db, user_id=user_id, upgrade_id=upgrade_id, lvl=1)
        return user_upgrade

    else:
        await process_upgrade(user, user_upgrade, upgrade, db)

        return user_upgrade


