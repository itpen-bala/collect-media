from aioredis import Redis

from app import config


async def get_redis_pool() -> Redis:
    redis_pool = await Redis.from_url(config.settings.redis.url)
    return redis_pool
