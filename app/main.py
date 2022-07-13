from loguru import logger

from app import app
from app.api.images import router
from app.config import settings
from app.storage.redis import get_redis_pool
from app.db.postgres import Database, CONN_KWARGS
from app.model.images import MediaBase

app.include_router(router)


@app.on_event('startup')
async def startup():
    logger.info('STARTUP...')
    app.state.db = Database(
        db_url=settings.postgresql.url,
        conn_kwargs=dict(**CONN_KWARGS),
    )
    await app.state.db.create_tables(MediaBase)
    app.state.redis = await get_redis_pool()


@app.on_event('shutdown')
async def shutdown_event():
    print('SHUTDOWN...')
    app.state.db.disconnect()
    await app.state.redis.close()
