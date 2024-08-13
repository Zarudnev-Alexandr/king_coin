import json
import os

from fastapi import APIRouter, Depends, HTTPException, Query, Path, UploadFile, File, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.added_funcs import decode_init_data
from app.cruds.upgrade import get_upgrade_category_by_name, create_upgrade_category, get_upgrade_category_by_id, \
    get_upgrade_by_name, add_upgrade, get_upgrade_by_id, get_all_upgrades_in_shop, get_all_upgrades, \
    get_all_upgrade_category, get_upgrade_level, add_upgrade_level, get_user_upgrades_by_upgrade_id, add_bought_upgrade, \
    process_upgrade, get_user_upgrades_in_this_category, create_combo, get_user_combo, get_latest_user_combo
from app.cruds.user import get_user, get_user_bool
from app.database import get_db
from app.models import UpgradeLevel, DailyCombo, UserDailyComboProgress, Upgrades
from app.schemas import UpgradeCategorySchema, CreateUpgradeSchema, UpgradeSchema, \
    UpgradeLevelSchema, UpgradeWithLevelsSchema, UserUpgradeCreateSchema, UserUpgradeSchema, CreateDailyComboSchema, \
    DailyComboSchema, UserDailyComboSchema, UpgradeCategoryBaseSchema, \
    UpgradeCategoryBaseSchemaWithId, ImageUploadResponse, UpgradeInfoSchema
from app.websockets.settings import ws_manager

upgrade_route = APIRouter()


@upgrade_route.post('/upgrade-category')
async def create_upgrade_category_func(upgrade_category_create: UpgradeCategoryBaseSchema,
                                       db: AsyncSession = Depends(get_db)) -> UpgradeCategoryBaseSchemaWithId:
    """
    Добавление категории, в которой хранятся апгрейды (Crypto, например) в БД
    """
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
async def get_upgrade_category_all(initData: str = Header(...),
                                   db: AsyncSession = Depends(get_db)) -> list[UpgradeCategorySchema]:
    """
    Все категории со всеми карточками для конкретного пользователя
    """
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    all_upgrade_categories = await get_all_upgrade_category(db)
    if not all_upgrade_categories:
        raise HTTPException(status_code=404, detail="Upgrade categories not found")

    all_categories_with_upgrades = []
    for upgrade_category_inc in all_upgrade_categories:

        upgrade_category = await get_upgrade_category_by_id(db, upgrade_category_id=upgrade_category_inc.id)
        user_upgrades_in_this_category = await get_user_upgrades_in_this_category(user.tg_id,
                                                                                  upgrade_category_inc.id,
                                                                                  db)
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
            upgrade.factor = current_upgrade_level.factor if current_upgrade_level else None
            upgrade.factor_at_new_lvl = next_upgrade_level.factor if next_upgrade_level else None

            upgrade.price_of_next_lvl = next_upgrade_level.price if next_upgrade_level else None

            filtered_upgrades.append(upgrade)

        upgrade_category.upgrades = filtered_upgrades

        all_categories_with_upgrades.append(upgrade_category)

    return all_categories_with_upgrades


@upgrade_route.post('/upgrade')
async def create_upgrade(upgrade_create: CreateUpgradeSchema,
                         db: AsyncSession = Depends(get_db)) -> UpgradeSchema:
    """
    Добавление апгрейда в БД
    """
    user_data = {
        "name": upgrade_create.name,
        "category_id": upgrade_create.category_id,
        "image_url": upgrade_create.image_url,
        "is_in_shop": upgrade_create.is_in_shop,
        "description": upgrade_create.description
    }

    upgrade = await get_upgrade_by_name(db, upgrade_name=upgrade_create.name)

    if upgrade:
        raise HTTPException(status_code=409, detail="this name is already in use")

    new_upgrade = await add_upgrade(db, **user_data)
    if new_upgrade:
        return new_upgrade
    else:
        raise HTTPException(status_code=400, detail="failed to create upgrade")


@upgrade_route.post('/upgrade-level')
async def create_upgrade(upgrade_level_create: UpgradeLevelSchema,
                         db: AsyncSession = Depends(get_db)) -> UpgradeLevelSchema:
    """
    Добавление уровней для апгрейдов в БД
    """
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
                      db: AsyncSession = Depends(get_db)):
    """
    Покупка апгрейда пользователем. Если апгрейд вообще не куплен, то выдается 1 уровень, если первый уровень есть,
    то просто идет прокачка
    """
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
        raise HTTPException(status_code=404, detail="List of levels is empty")

    user_upgrade = await get_user_upgrades_by_upgrade_id(user_id, upgrade_id, db)

    if not user_upgrade:
        user_upgrade = await add_bought_upgrade(db, user, upgrade, lvl=1)
        new_upgrade_purchased = True
    else:
        await process_upgrade(user, user_upgrade, upgrade, db)
        new_upgrade_purchased = False

    combo_status = {
        "new_combo_created": False,
        "upgrade_1_purchased": False,
        "upgrade_2_purchased": False,
        "upgrade_3_purchased": False,
        "combo_completed": False,
        "reward_claimed": False
    }

    # Check the latest daily combo
    latest_combo = await db.execute(select(DailyCombo).order_by(DailyCombo.created.desc()).limit(1))
    latest_combo = latest_combo.scalars().first()

    if latest_combo:
        # Check if the bought upgrade is part of the daily combo
        user_combo_progress = await db.execute(
            select(UserDailyComboProgress)
            .filter_by(user_id=user_id, combo_id=latest_combo.id)
        )
        user_combo_progress = user_combo_progress.scalars().first()

        if upgrade_id in [latest_combo.upgrade_1_id, latest_combo.upgrade_2_id, latest_combo.upgrade_3_id]:
            if not user_combo_progress:
                user_combo_progress = UserDailyComboProgress(user_id=user_id, combo_id=latest_combo.id)
                db.add(user_combo_progress)
                combo_status["new_combo_created"] = True

            if upgrade_id == latest_combo.upgrade_1_id and not user_combo_progress.upgrade_1_bought:
                user_combo_progress.upgrade_1_bought = True
                combo_status["upgrade_1_purchased"] = True
            elif upgrade_id == latest_combo.upgrade_2_id and not user_combo_progress.upgrade_2_bought:
                user_combo_progress.upgrade_2_bought = True
                combo_status["upgrade_2_purchased"] = True
            elif upgrade_id == latest_combo.upgrade_3_id and not user_combo_progress.upgrade_3_bought:
                user_combo_progress.upgrade_3_bought = True
                combo_status["upgrade_3_purchased"] = True

            # Check if all upgrades are bought and grant reward
            if (user_combo_progress.upgrade_1_bought and
                    user_combo_progress.upgrade_2_bought and
                    user_combo_progress.upgrade_3_bought and
                    not user_combo_progress.reward_claimed):
                user.money += latest_combo.reward
                user_combo_progress.reward_claimed = True
                combo_status["combo_completed"] = True
                combo_status["reward_claimed"] = True

            await db.commit()
            await db.refresh(user_combo_progress)

    await db.refresh(user_upgrade)

    next_upgrade_level = await db.execute(
        select(UpgradeLevel).filter_by(upgrade_id=upgrade.id, lvl=user_upgrade.lvl + 1)
    )
    next_upgrade_level = next_upgrade_level.scalars().first()

    current_upgrade_level = await db.execute(
        select(UpgradeLevel).filter_by(upgrade_id=upgrade.id, lvl=user_upgrade.lvl)
    )
    current_upgrade_level = current_upgrade_level.scalars().first()

    return_data = {
        "user_remaining_money": user.money,
        "upgrade_id": upgrade.id,
        "current_lvl": current_upgrade_level.lvl if current_upgrade_level else None,
        "current_factor": current_upgrade_level.factor if current_upgrade_level else None,
        "factor_at_new_lvl": next_upgrade_level.factor if next_upgrade_level else None,
        "price_of_next_lvl": next_upgrade_level.price if next_upgrade_level else None,
        "next_lvl": next_upgrade_level.lvl if next_upgrade_level else None,
        "combo_status": combo_status if latest_combo else {}  # Only include combo_status if there's a combo
    }

    await ws_manager.notify_user(user.tg_id, {
        "event": "buy_upgrade",
        "data": {
            "user_remaining_money": user.money,
            "upgrade_id": upgrade.id,
            "current_lvl": current_upgrade_level.lvl if current_upgrade_level else None,
            "current_factor": current_upgrade_level.factor if current_upgrade_level else None,
            "factor_at_new_lvl": next_upgrade_level.factor if next_upgrade_level else None,
            "price_of_next_lvl": next_upgrade_level.price if next_upgrade_level else None,
            "next_lvl": next_upgrade_level.lvl if next_upgrade_level else None,
            "combo_status": {
                "new_combo_created": combo_status["new_combo_created"],
                "upgrade_1_purchased": combo_status["upgrade_1_purchased"],
                "upgrade_2_purchased": combo_status["upgrade_2_purchased"],
                "upgrade_3_purchased": combo_status["upgrade_3_purchased"],
                "combo_completed": combo_status["combo_completed"],
                "reward_claimed": combo_status["reward_claimed"]
            } if latest_combo else {}
        }
    })

    return return_data


@upgrade_route.post('/create-daily-combo')
async def create_daily_combo(daily_combo_create: CreateDailyComboSchema,
                             db: AsyncSession = Depends(get_db)) -> DailyComboSchema:
    """
    Создание дневного комбо. Комбо не обязательно работает один день, просто подразумевается, что менять его будут
    раз в день) Вносим сюда 3 разных апгрейда и награду
    """

    user_data = {
        "upgrade_1_id": daily_combo_create.upgrade_1_id,
        "upgrade_2_id": daily_combo_create.upgrade_2_id,
        "upgrade_3_id": daily_combo_create.upgrade_3_id,
        "reward": daily_combo_create.reward,
    }
    new_combo = await create_combo(db, **user_data)
    return new_combo


@upgrade_route.get("/user-combo")
async def get_user_combo_progress(initData: str = Header(...),
                                  db: AsyncSession = Depends(get_db)) -> UserDailyComboSchema:
    """
    Получение информации о текущем состоянии дневного комбо конкретного пользователя
    """
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    latest_combo = await get_latest_user_combo(db)

    if not latest_combo:
        raise HTTPException(status_code=404, detail="Daily combo not found")

    user_combo = await get_user_combo(db, user.tg_id, latest_combo)

    if not user_combo:
        raise HTTPException(status_code=200, detail="User didn't buy any cards from combo today")

    # Функция для получения данных об улучшении или None
    async def get_upgrade_info(upgrade_id, is_bought):
        if is_bought:
            upgrade = await get_upgrade_by_id(db, upgrade_id)
            return UpgradeInfoSchema(
                is_bought=is_bought,
                image_url=upgrade.image_url if upgrade else None,
                name=upgrade.name if upgrade else None,
                id=upgrade.id if upgrade else None
            )
        else:
            return UpgradeInfoSchema(is_bought=is_bought)

    # Получение информации об улучшениях
    upgrade_1_info = await get_upgrade_info(latest_combo.upgrade_1_id, user_combo.upgrade_1_bought)
    upgrade_2_info = await get_upgrade_info(latest_combo.upgrade_2_id, user_combo.upgrade_2_bought)
    upgrade_3_info = await get_upgrade_info(latest_combo.upgrade_3_id, user_combo.upgrade_3_bought)

    combo_data = DailyComboSchema(
        id=latest_combo.id,
        upgrade_1_id=latest_combo.upgrade_1_id,
        upgrade_2_id=latest_combo.upgrade_2_id,
        upgrade_3_id=latest_combo.upgrade_3_id,
        reward=latest_combo.reward
    )

    return UserDailyComboSchema(
        user_id=user.tg_id,
        combo_id=latest_combo.id,
        upgrade_1=upgrade_1_info,
        upgrade_2=upgrade_2_info,
        upgrade_3=upgrade_3_info,
        reward_claimed=user_combo.reward_claimed,
        combo=combo_data
    )


@upgrade_route.post('/upgrade/{upgrade_id}/upload_image', response_model=ImageUploadResponse)
async def upload_image(upgrade_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """
    Добавление изображения к апгрейдам
    """
    # Проверка, существует ли апгрейд
    upgrade = await db.get(Upgrades, upgrade_id)
    if not upgrade:
        raise HTTPException(status_code=404, detail="Upgrade not found")

    # Генерация уникального имени файла
    file_extension = file.filename.split(".")[-1]
    file_name = f"{upgrade_id}.{file_extension}"

    # Сохранение файла на сервере
    file_path = os.path.join("/app/uploads", file_name)  # Оставляем путь как в контейнере
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Обновление записи в базе данных
    upgrade.image_url = file_path
    await db.commit()

    return ImageUploadResponse(image_url=file_path)
