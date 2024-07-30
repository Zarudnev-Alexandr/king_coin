import asyncio

from fastapi import APIRouter, WebSocket,WebSocketDisconnect, WebSocketException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.upgrade import get_user_upgrades, get_upgrade_by_id
from app.cruds.user import get_user, update_user_level
from app.database import sessionmanager, get_db, get_db_for_websockets
from app.models import Level
from app.websockets.settings import ws_manager

websocket_router = APIRouter()


async def user_income_task(user_id: int, db: AsyncSession, user, levels_list):
    while True:
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
        print('😙😙😙', total_hourly_income, flush=True)

        # Доход за каждые 5 секунд (1/720 от часового дохода)
        income_per_interval = total_hourly_income / 720

        user.money += income_per_interval
        await db.commit()
        await db.refresh(user)

        # Проверка на достижение новых уровней
        new_levels = []
        for level in levels_list:
            await db.refresh(level)
            if user.money >= level.required_money:
                old_lvl = user.lvl
                user.lvl = level.lvl
                user.taps_for_level = level.taps_for_level
                await db.commit()
                await db.refresh(user)
                await ws_manager.send_message(
                    {"event": "new_lvl", "data": {"old_lvl": old_lvl,
                                                  "new_lvl": user.lvl,
                                                  "new_taps_for_lvl": user.taps_for_level}},
                    user_id)
            else:
                new_levels.append(level)

        levels_list[:] = new_levels

        # Определение денег до следующего уровня
        if levels_list:
            next_level_money = levels_list[0].required_money
            money_to_next_level = next_level_money - user.money
        else:
            next_level_money = None
            money_to_next_level = None

        # Отправка обновленного значения денег и информации о доходах пользователю
        await ws_manager.send_message(
            {"event": "update",
             "data": {"money": user.money,
                      "hourly_income": total_hourly_income,
                      "money_to_next_level": money_to_next_level}},
            user_id
        )

        # Ожидание 5 секунд перед следующей отправкой
        await asyncio.sleep(5)


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
            ws_manager.disconnect(user_id)
        finally:
            ws_manager.disconnect(user_id)


# @websocket_router.websocket("/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: int):
#     async with get_db_for_websockets() as db:
#         user = await get_user(db, user_id)
#         if not user:
#             raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA)
#
#         user_upgrades = await get_user_upgrades(user.tg_id, db)
#         upgrades = await asyncio.gather(
#             *[get_upgrade_by_id(db, user_upgrade.upgrade_id) for user_upgrade in user_upgrades]
#         )
#
#         total_hourly_income = sum(
#             next((lvl.factor for lvl in upgrade.levels if lvl.lvl == user_upgrade.lvl), 0)
#             for user_upgrade, upgrade in zip(user_upgrades, upgrades)
#         )
#
#         # Доход за каждые 5 секунд (1/720 от часового дохода)
#         income_per_interval = total_hourly_income / 720
#
#         print('😍😍😍😍😍', user.__dict__, flush=True)
#         try:
#             await ws_manager.connect(user_id, websocket)
#             while True:
#                 # Обновление денег пользователя
#                 user.money += income_per_interval
#
#                 # Проверка и обновление уровня пользователя
#                 old_level = user.lvl
#                 next_level = await update_user_level(db, user)
#                 if next_level and next_level.lvl != old_level:
#                     await ws_manager.send_message({"old_level": old_level, "new_level": next_level.lvl}, user_id)
#                     user.lvl = next_level.lvl
#
#                 await db.commit()
#                 await db.refresh(user)
#
#                 # Отправка обновленного значения денег пользователю
#                 await ws_manager.send_message({"money": user.money}, user_id)
#
#                 await asyncio.sleep(5)
#         except WebSocketDisconnect:
#             await ws_manager.disconnect(user_id)