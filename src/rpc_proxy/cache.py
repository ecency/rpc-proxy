from typing import Any

from aiocache import caches

caches.set_config({
    'default': {
        'cache': "aiocache.SimpleMemoryCache",
        'serializer': {
            'class': "aiocache.serializers.StringSerializer"
        }
    }
})


async def cache_get(key: str):
    cache = caches.get('default')
    return await cache.get(key)


async def cache_set(key: str, value: Any, ttl: int):
    cache = caches.get('default')
    await cache.set(key, value, ttl)
