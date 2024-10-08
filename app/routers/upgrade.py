import json
import logging
import os

from environs import Env
from fastapi import APIRouter, Depends, HTTPException, Query, Path, UploadFile, File, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.added_funcs import decode_init_data, user_check_and_update_without_init_data, \
    user_check_and_update_without_init_data_only_money, log_execution_time
from app.cruds.task import get_invited_count, check_telegram_subscription
from app.cruds.upgrade import get_upgrade_category_by_name, create_upgrade_category, get_upgrade_category_by_id, \
    get_upgrade_by_name, add_upgrade, get_upgrade_by_id, get_all_upgrades_in_shop, get_all_upgrades, \
    get_all_upgrade_category, get_upgrade_level, add_upgrade_level, get_user_upgrades_by_upgrade_id, add_bought_upgrade, \
    process_upgrade, get_user_upgrades_in_this_category, create_combo, get_user_combo, get_latest_user_combo, \
    get_cached_all_upgrade_categories, get_user_upgrades_for_all_categories, get_sorted_filtered_upgrades, \
    check_conditions, get_cached_latest_daily_combo
from app.cruds.user import get_user, get_user_bool
from app.database import get_db
from app.models import UpgradeLevel, DailyCombo, UserDailyComboProgress, Upgrades, UpgradeConditionType
from app.schemas import UpgradeCategorySchema, CreateUpgradeSchema, UpgradeSchema, \
    UpgradeLevelSchema, UpgradeWithLevelsSchema, UserUpgradeCreateSchema, UserUpgradeSchema, CreateDailyComboSchema, \
    DailyComboSchema, UserDailyComboSchema, UpgradeCategoryBaseSchema, \
    UpgradeCategoryBaseSchemaWithId, ImageUploadResponse, UpgradeInfoSchema
from app.websockets.settings import ws_manager

upgrade_route = APIRouter()

env = Env()
env.read_env()

SERVER_URL = env('SERVER_URL')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# @upgrade_route.post('/upgrade-category')
# async def create_upgrade_category_func(upgrade_category_create: UpgradeCategoryBaseSchema,
#                                        db: AsyncSession = Depends(get_db)) -> UpgradeCategoryBaseSchemaWithId:
#     """
#     Добавление категории, в которой хранятся апгрейды (Crypto, например) в БД
#     """
#     user_data = {
#         "category": upgrade_category_create.category
#     }
#     upgrade_category = await get_upgrade_category_by_name(db, upgrade_category_name=upgrade_category_create.category)
#
#     if upgrade_category:
#         raise HTTPException(status_code=409, detail="this name is already in use")
#
#     new_upgrade_category = await create_upgrade_category(db, **user_data)
#     if new_upgrade_category:
#         return new_upgrade_category
#     else:
#         raise HTTPException(status_code=400, detail="failed to create upgrade category")


@upgrade_route.get('/upgrade-category/all')
async def get_upgrade_category_all(initData: str = Header(...),
                                   db: AsyncSession = Depends(get_db)) -> list[UpgradeCategorySchema]:
    """
    Все категории со всеми карточками для конкретного пользователя
    """
    logger.info(f"**get_upgrade_category_all**---------------------")
    init_data_decode = await log_execution_time(decode_init_data)(initData, db)
    user = init_data_decode["user"]

    all_upgrade_categories = await log_execution_time(get_cached_all_upgrade_categories)(db)
    if not all_upgrade_categories:
        raise HTTPException(status_code=404, detail="Upgrade categories not found")

    user_upgrades_dict = await log_execution_time(get_user_upgrades_for_all_categories)(user.tg_id, db)

    all_upgrades = []
    for upgrade_category in all_upgrade_categories:
        for upgrade in upgrade_category.upgrades:
            all_upgrades += [upgrade]

    for upgrade_category in all_upgrade_categories:
        for upgrade in upgrade_category.upgrades:
            user_upgrade = user_upgrades_dict.get(upgrade.id, None)
            if user_upgrade:
                upgrade.lvl = user_upgrade["lvl"]
                upgrade.is_bought = user_upgrade["is_bought"]
            else:
                upgrade.lvl = 0
                upgrade.is_bought = False

            current_level_data = None
            next_level_data = None

            # инфа о текущем и следующем уровнях
            for level in upgrade.levels:
                if level.lvl == upgrade.lvl:
                    current_level_data = level
                elif level.lvl == upgrade.lvl + 1:
                    next_level_data = level

            if current_level_data:
                upgrade.factor = current_level_data.factor
            else:
                upgrade.factor = None

            if next_level_data:
                upgrade.factor_at_new_lvl = next_level_data.factor
                upgrade.price_of_next_lvl = next_level_data.price
            else:
                upgrade.factor_at_new_lvl = None
                upgrade.price_of_next_lvl = None

            # Задания на карточки
            if upgrade.conditions:
                condition_result = await log_execution_time(check_conditions)(user, all_upgrades, upgrade.conditions[0], db)
                if condition_result:
                    upgrade.conditions_met = condition_result['conditions_met']
                    upgrade.unmet_conditions = condition_result['unmet_conditions']
            else:
                upgrade.conditions_met = True
                upgrade.unmet_conditions = []

    return all_upgrade_categories


# @upgrade_route.post('/upgrade')
# async def create_upgrade(upgrade_create: CreateUpgradeSchema,
#                          db: AsyncSession = Depends(get_db)) -> UpgradeSchema:
#     """
#     Добавление апгрейда в БД
#     """
#     user_data = {
#         "name": upgrade_create.name,
#         "category_id": upgrade_create.category_id,
#         "image_url": upgrade_create.image_url,
#         "is_in_shop": upgrade_create.is_in_shop,
#         "description": upgrade_create.description,
#         "english_description": upgrade_create.english_description,
#         "sort_position": upgrade_create.sort_position,
#     }
#
#     upgrade = await get_upgrade_by_name(db, upgrade_name=upgrade_create.name)
#
#     if upgrade:
#         raise HTTPException(status_code=409, detail="this name is already in use")
#
#     new_upgrade = await add_upgrade(db, **user_data)
#     if new_upgrade:
#         return new_upgrade
#     else:
#         raise HTTPException(status_code=400, detail="failed to create upgrade")


# @upgrade_route.post('/upgrade-level')
# async def create_upgrade(upgrade_level_create: UpgradeLevelSchema,
#                          db: AsyncSession = Depends(get_db)) -> UpgradeLevelSchema:
#     """
#     Добавление уровней для апгрейдов в БД
#     """
#     user_data = {
#         "upgrade_id": upgrade_level_create.upgrade_id,
#         "lvl": upgrade_level_create.lvl,
#         "factor": upgrade_level_create.factor,
#         "price": upgrade_level_create.price
#     }
#
#     if upgrade_level_create.lvl < 1:
#         raise HTTPException(status_code=400, detail="level cannot be less than 1")
#
#     upgrade = await get_upgrade_by_id(db, upgrade_id=upgrade_level_create.upgrade_id)
#
#     if not upgrade:
#         raise HTTPException(status_code=404, detail="upgrade not found")
#
#     upgrade_level = await get_upgrade_level(upgrade_level_create.upgrade_id, upgrade_level_create.lvl, db)
#
#     if upgrade_level:
#         raise HTTPException(status_code=409, detail="this upgrade level is already in use")
#
#     new_upgrade_level = await add_upgrade_level(db, **user_data)
#     if new_upgrade_level:
#         return new_upgrade_level
#     else:
#         raise HTTPException(status_code=400, detail="failed to create upgrade level")


@upgrade_route.post('/buy-upgrade')
async def buy_upgrade(user_upgrade_create: UserUpgradeCreateSchema,
                      db: AsyncSession = Depends(get_db)):
    """
    Покупка апгрейда пользователем. Если апгрейд вообще не куплен, то выдается 1 уровень, если первый уровень есть,
    то просто идет прокачка
    """
    logger.info(f"**buy_upgrade**---------------------")
    user_id = user_upgrade_create.user_id
    upgrade_id = user_upgrade_create.upgrade_id

    user = await log_execution_time(get_user)(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await log_execution_time(user_check_and_update_without_init_data_only_money)(user, db)

    upgrade = await log_execution_time(get_upgrade_by_id)(db, upgrade_id)
    if not upgrade:
        raise HTTPException(status_code=404, detail="Upgrade not found")

    if not upgrade.is_in_shop:
        raise HTTPException(status_code=404, detail="Upgrade not in shop")

    if len(upgrade.levels) < 1:
        raise HTTPException(status_code=404, detail="List of levels is empty")

    conditions = upgrade.conditions
    for condition in conditions:
        if condition.condition_type == UpgradeConditionType.INVITE:
            invited_count = await log_execution_time(get_invited_count)(db, user.tg_id)
            if invited_count < condition.condition_value:
                raise HTTPException(status_code=400, detail=f"You need to invite {condition.condition_value} friends")

        elif condition.condition_type == UpgradeConditionType.REACH_UPGRADE_LEVEL:
            related_upgrade = await log_execution_time(get_user_upgrades_by_upgrade_id)(user_id, condition.related_upgrade_id, db)
            if not related_upgrade or related_upgrade.lvl < condition.condition_value:
                raise HTTPException(status_code=400,
                                    detail=f"You need to reach level {condition.condition_value} of upgrade {condition.related_upgrade_id}")

        elif condition.condition_type == UpgradeConditionType.SUBSCRIBE_TELEGRAM:
            is_subscribed = check_telegram_subscription(int(condition.channel_url), user.tg_id)
            if not is_subscribed:
                raise HTTPException(status_code=400, detail=f"You need to subscribe to {condition.channel_url}")

    user_upgrade = await log_execution_time(get_user_upgrades_by_upgrade_id)(user_id, upgrade_id, db)

    if not user_upgrade:
        user_upgrade = await log_execution_time(add_bought_upgrade)(db, user, upgrade, lvl=1)
        new_upgrade_purchased = True
    else:
        await log_execution_time(process_upgrade)(user, user_upgrade, upgrade, db)
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
    latest_combo = await log_execution_time(get_cached_latest_daily_combo)(db)

    if latest_combo:
        # Check if the bought upgrade is part of the daily combo
        user_combo_progress = await log_execution_time(db.execute)(
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

            await log_execution_time(db.commit)()
            await log_execution_time(db.refresh)(user_combo_progress)

    await log_execution_time(db.refresh)(user_upgrade)

    current_upgrade_lvl_data = None
    next_upgrade_lvl_data = None

    for level in upgrade.levels:
        if level.lvl == user_upgrade.lvl:
            current_upgrade_lvl_data = {
                "lvl": level.lvl,
                "factor": level.factor
            }
        elif level.lvl == user_upgrade.lvl + 1:
            next_upgrade_lvl_data = {
                "lvl": level.lvl,
                "factor": level.factor,
                "price": level.price
            }

    # Если текущий уровень не найден, это может быть первый уровень
    if not current_upgrade_lvl_data:
        current_upgrade_lvl_data = {
            "lvl": None,  # или 0, если нужен дефолтный уровень
            "factor": None
        }

    # Если следующий уровень не найден, значит это последний уровень
    if not next_upgrade_lvl_data:
        next_upgrade_lvl_data = {
            "lvl": None,
            "factor": None,
            "price": None
        }

    user_check = await log_execution_time(user_check_and_update_without_init_data)(user, db)
    await log_execution_time(db.refresh)(upgrade)
    return_data = {
        "user_remaining_money": user.money,
        "upgrade_id": upgrade.id,
        "current_lvl": current_upgrade_lvl_data["lvl"] if current_upgrade_lvl_data else None,
        "current_factor": current_upgrade_lvl_data["factor"] if current_upgrade_lvl_data else None,
        "factor_at_new_lvl": next_upgrade_lvl_data["factor"] if next_upgrade_lvl_data else None,
        "price_of_next_lvl": next_upgrade_lvl_data["price"] if next_upgrade_lvl_data else None,
        "next_lvl": next_upgrade_lvl_data["lvl"] if next_upgrade_lvl_data else None,
        "combo_status": combo_status if latest_combo else {},
        "user_check": user_check
    }

    return return_data


@upgrade_route.get('/can-i-buy-upgrade')
async def can_i_buy_this_upgrade(upgrade_id: int,
                                 initData: str = Header(...),
                                 db: AsyncSession = Depends(get_db)):
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    upgrade = await get_upgrade_by_id(db, upgrade_id)
    if not upgrade:
        raise HTTPException(status_code=404, detail="Upgrade not found")

    if not upgrade.is_in_shop:
        raise HTTPException(status_code=404, detail="Upgrade not in shop")

    if len(upgrade.levels) < 1:
        raise HTTPException(status_code=404, detail="List of levels is empty")

    conditions = upgrade.conditions
    for condition in conditions:
        if condition.condition_type == UpgradeConditionType.INVITE:
            invited_count = await get_invited_count(db, user.tg_id)
            if invited_count < condition.condition_value:
                raise HTTPException(status_code=400, detail=f"You need to invite {condition.condition_value} friends")

        elif condition.condition_type == UpgradeConditionType.REACH_UPGRADE_LEVEL:
            related_upgrade = await get_user_upgrades_by_upgrade_id(user.tg_id, condition.related_upgrade_id, db)
            if not related_upgrade or related_upgrade.lvl < condition.condition_value:
                raise HTTPException(status_code=400,
                                    detail=f"You need to reach level {condition.condition_value} of upgrade {condition.related_upgrade_id}")

        elif condition.condition_type == UpgradeConditionType.SUBSCRIBE_TELEGRAM:
            is_subscribed = check_telegram_subscription(int(condition.channel_url), user.tg_id)
            if not is_subscribed:
                raise HTTPException(status_code=400, detail=f"You need to subscribe to {condition.description}")
        return HTTPException(status_code=200, detail=f"ok")


# @upgrade_route.post('/create-daily-combo')
# async def create_daily_combo(daily_combo_create: CreateDailyComboSchema,
#                              db: AsyncSession = Depends(get_db)) -> DailyComboSchema:
#     """
#     Создание дневного комбо. Комбо не обязательно работает один день, просто подразумевается, что менять его будут
#     раз в день) Вносим сюда 3 разных апгрейда и награду
#     """
#
#     user_data = {
#         "upgrade_1_id": daily_combo_create.upgrade_1_id,
#         "upgrade_2_id": daily_combo_create.upgrade_2_id,
#         "upgrade_3_id": daily_combo_create.upgrade_3_id,
#         "reward": daily_combo_create.reward,
#     }
#     new_combo = await create_combo(db, **user_data)
#     return new_combo


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
async def upload_image(upgrade_id: int,
                       initData: str = Header(...),
                       file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """
    Добавление изображения к апгрейдам
    """
    init_data_decode = await decode_init_data(initData, db)
    user = init_data_decode["user"]

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can use this API")

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
    upgrade.image_url = f"{SERVER_URL}/uploads/{file_name}"
    await db.commit()

    return ImageUploadResponse(image_url=file_path)
