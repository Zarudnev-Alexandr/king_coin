import os
from typing import Optional

import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:test@db:5432/king_coin")


async def select_user(user_id: int) -> Optional[dict]:
    conn = await asyncpg.connect(dsn=DATABASE_URL)
    try:
        result = await conn.fetchrow('SELECT * FROM "user" WHERE tg_id = $1', user_id)
        return dict(result) if result else None
    finally:
        await conn.close()


async def check_args(args, user_id: int):
    if args == '':
        args = '0'
        return args
    elif not args.isnumeric():
        args = '0'
        return args
    elif args.isnumeric():
        if int(args) == user_id:
            args = '0'
            return args
        elif await select_user(user_id=int(args)) is None:
            args = '0'
            return args
        else:
            args = str(args)
            return args
    else:
        args = '0'
        return args
