import json
import time
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text

from rpc_proxy.util import assert_env_vars

db_url = assert_env_vars('DB_URL')

db_engine = create_async_engine("postgresql+asyncpg://{}".format(db_url))


def create_cache():
    sql = """ CREATE TABLE IF NOT EXISTS public.cache(
    "key" VARCHAR NOT NULL,
    "value" JSON,
    "ttl" BIGINT NOT NULL,
    "created" BIGINT NOT NULL
    );
    CREATE UNIQUE INDEX IF NOT EXISTS cache_key_uindex ON public.cache (key);
    """

    create_engine("postgresql://{}".format(db_url)).execute(sql)
    print("OK")


async def cache_get(key: str):
    async with db_engine.connect() as conn:
        result = (await conn.execute(text('SELECT "value", ttl from cache where key=:key'), {"key": key})).first()
        if result is None:
            await conn.close()
            return None

        if result.ttl < time.time():
            await conn.execute(text("DELETE FROM cache WHERE key=:key"), {"key": key})
            await conn.commit()
            await conn.close()
            return None

        await conn.close()
        return result.value


async def cache_set(key: str, value: Any, ttl: int):
    async with db_engine.connect() as conn:
        result = (await conn.execute(text('SELECT "value", ttl from cache where key=:key'), {"key": key})).first()
        if result is not None:
            await conn.execute(text("DELETE FROM cache WHERE key=:key"), {"key": key})

        ts = int(time.time())
        cache_ttl = ts + ttl
        args = {"key": key, "value": json.dumps(value), "ttl": cache_ttl, "created": ts}
        await conn.execute(text('INSERT INTO cache ("key", "value", ttl, created) VALUES(:key, :value, :ttl, :created)'), args)
        await conn.commit()
        await conn.close()
