from typing import Any

from aiocache import caches

caches.set_config({
    'default': {
        'cache': "aiocache.RedisCache",
        'endpoint': "127.0.0.1",
        'port': 6379,
        'serializer': {
            'class': "aiocache.serializers.PickleSerializer"
        },
    }
})


async def cache_get(key: str):
    cache = caches.get('default')
    return await cache.get(key)


async def cache_set(key: str, value: Any, ttl: int):
    cache = caches.get('default')
    await cache.set(key, value, ttl)
