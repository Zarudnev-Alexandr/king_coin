import asyncio

from fastapi import APIRouter, WebSocket,WebSocketDisconnect, WebSocketException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.upgrade import get_user_upgrades, get_upgrade_by_id
from app.cruds.user import get_user, update_user_level
from app.database import sessionmanager, get_db, get_db_for_websockets
from app.models import Level
from app.websockets.settings import ws_manager
import logging

websocket_router = APIRouter()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def user_income_task(user_id: int, db: AsyncSession, user, levels_list):
    referral_rewards = {
        1: {"no_premium": 15000, "premium": 25000},
        2: {"no_premium": 35000, "premium": 55000},
        3: {"no_premium": 40000, "premium": 65000},
        4: {"no_premium": 65000, "premium": 90000},
        5: {"no_premium": 95000, "premium": 140000},
        6: {"no_premium": 200000, "premium": 400000},
        7: {"no_premium": 500000, "premium": 1000000},
        8: {"no_premium": 1500000, "premium": 3000000},
        9: {"no_premium": 3500000, "premium": 6000000},
        10: {"no_premium": 10000000, "premium": 20000000},
    }

    while True:
        try:
            # Обновление данных пользователя перед каждым циклом
            await db.refresh(user)

            # Получение всех апгрейдов пользователя
            user_upgrades = await get_user_upgrades(user.tg_id, db)
            upgrades = await asyncio.gather(
                *[get_upgrade_by_id(db, user_upgrade.upgrade_id) for user_upgrade in user_upgrades]
            )

            # Пересчет общего дохода
            total_hourly_income = sum(
                next((lvl.factor for lvl in upgrade.levels if lvl.lvl == user_upgrade.lvl), 0)
                for user_upgrade, upgrade in zip(user_upgrades, upgrades)
            )

            # Доход за каждые 5 секунд (1/720 от часового дохода)
            income_per_interval = total_hourly_income / 360

            # Обновление денег пользователя
            user.money += income_per_interval
            await db.commit()
            await db.refresh(user)

            # Проверка на достижение новых уровней
            # new_levels = []
            for level in levels_list:
                await db.refresh(level)
                if user.money >= level.required_money and user.lvl < level.lvl:
                    old_lvl = user.lvl
                    user.lvl = level.lvl
                    user.taps_for_level = level.taps_for_level
                    await db.commit()
                    await db.refresh(user)

                    # Начисление бонусов пригласившему
                    if user.invited_tg_id:
                        inviter = await get_user(db, user.invited_tg_id)
                        if inviter:
                            reward = referral_rewards.get(user.lvl, {}).get("premium" if user.is_premium else "no_premium", 0)
                            inviter.money += reward
                            await db.commit()
                            await db.refresh(inviter)

                            try:
                                await db.refresh(user)
                                await ws_manager.send_message(
                                    {"event": "referral_reward", "data": {"referral_level": user.lvl, "reward": reward}},
                                    inviter.tg_id
                                )
                            except Exception as e:
                                logger.error(f"Failed to send referral reward message: {e}")

                    await ws_manager.send_message(
                        {"event": "new_lvl", "data": {"old_lvl": old_lvl,
                                                      "new_lvl": user.lvl,
                                                      "new_taps_for_lvl": user.taps_for_level}},
                        user_id)
            #     else:
            #         new_levels.append(level)
            #
            # levels_list[:] = new_levels

            # Определение денег до следующего уровня
            # if levels_list:
            #     next_level_money = levels_list[0].required_money
            #     money_to_next_level = next_level_money - user.money
            # else:
            #     next_level_money = None
            #     money_to_next_level = None

            next_level = next((level for level in levels_list if level.lvl > user.lvl), None)
            money_to_next_level = next_level.required_money - user.money if next_level else None

            # Отправка обновленного значения денег и информации о доходах пользователю
            await ws_manager.send_message(
                {"event": "update",
                 "data": {"money": int(user.money),
                          "hourly_income": total_hourly_income,
                          "money_to_next_level": money_to_next_level}},
                user_id
            )

            # Логирование отправленных данных
            logger.info(f"Sent update to user {user_id}: money={int(user.money)}, hourly_income={total_hourly_income}, money_to_next_level={money_to_next_level}")

            # Ожидание 10 секунд перед следующей отправкой
            await asyncio.sleep(10)

        except Exception as e:
            logger.error(f"Error in user_income_task for user {user_id}: {e}")
            await db.rollback()
            await asyncio.sleep(10)  # Немного подождем перед повтором цикла в случае ошибки

@websocket_router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    async with get_db_for_websockets() as db:
        user = await get_user(db, user_id)

        if not user:
            await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
            return

        levels = await db.execute(select(Level).order_by(Level.lvl))
        levels = levels.unique().scalars().all()

        levels_list = [level for level in levels if level.lvl > user.lvl]

        try:
            await ws_manager.connect(user_id, websocket)

            # Запуск задачи для обновления дохода пользователя
            task = asyncio.create_task(user_income_task(user_id, db, user, levels_list))
            ws_manager.tasks[user_id] = task

            # Ожидание сообщений от клиента
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected for user {user_id}")
            ws_manager.disconnect(user_id)
        finally:
            ws_manager.disconnect(user_id)
            if task:
                task.cancel()  # Отменяем задачу при отключении вебсокета
                try:
                    await task
                except asyncio.CancelledError:
                    logger.info(f"Task for user {user_id} cancelled")

