from loguru import logger

from config import app
from api.images import router
from storage.redis import get_redis_pool
from db.base import database

app.include_router(router)


@app.on_event('startup')
async def startup():
    logger.info('STARTUP')
    app.state.redis = await get_redis_pool()
    await database.connect()


@app.on_event('shutdown')
async def shutdown_event():
    print('SHUTDOWN')
    await app.state.redis.close()
    await database.disconnect()
