import asyncio

from fastapi import APIRouter, WebSocket,WebSocketDisconnect, WebSocketException, status, Depends

from app.cruds.upgrade import get_user_upgrades, get_upgrade_by_id
from app.cruds.user import get_user
from app.database import sessionmanager, get_db, get_db_for_websockets
from app.websockets.settings import ws_manager

websocket_router = APIRouter()


# async def websocket_endpoint(
#         websocket: WebSocket,
#         user_id: int
# ):
#     async with get_db() as db:
#         user = await get_user(db, user_id)
#
#         if not user:
#             raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA)


@websocket_router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    async with get_db_for_websockets() as db:
        user = await get_user(db, user_id)
        if not user:
            raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA)

        user_upgrades = await get_user_upgrades(user.tg_id, db)
        upgrades = await asyncio.gather(
            *[get_upgrade_by_id(db, user_upgrade.upgrade_id) for user_upgrade in user_upgrades]
        )

        total_hourly_income = sum(
            next((lvl.factor for lvl in upgrade.levels if lvl.lvl == user_upgrade.lvl), 0)
            for user_upgrade, upgrade in zip(user_upgrades, upgrades)
        )

        # Доход за каждые 5 секунд (1/720 от часового дохода)
        income_per_interval = total_hourly_income / 720

        print('😍😍😍😍😍', user.__dict__, flush=True)
        try:
            await ws_manager.connect(user_id, websocket)
            while True:
                # Обновление денег пользователя
                user.money += income_per_interval
                await db.commit()
                await db.refresh(user)

                # Отправка обновленного значения денег пользователю
                await ws_manager.send_message({"money": user.money}, user_id)

                await asyncio.sleep(5)
        except WebSocketDisconnect:
            await ws_manager.disconnect(user_id)




    # await websocket.accept()
    # try:
    #     while True:
    #         print(f"Starting DB transaction for user_id {user_id}")
    #         async with get_db_for_websockets() as db:
    #             print(f"Fetching user {user_id} from database")
    #             user = await get_user(db, user_id)
    #             if user:
    #                 # Обновление денег пользователя
    #                 user.money += user.current_factor  # Пример обновления
    #                 print(f"User {user_id} money updated to {user.money}")
    #                 await db.commit()
    #                 # Отправка обновленных данных на фронтенд
    #                 await websocket.send_json({"money": user.money})
    #             else:
    #                 print(f"User {user_id} not found")
    #         await asyncio.sleep(2)  # Обновление каждые 2 секунды
    # except WebSocketDisconnect:
    #     print(f"User {user_id} disconnected")
    # except Exception as e:
    #     print(f"Error: {e}")