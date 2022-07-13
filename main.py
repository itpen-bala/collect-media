from fastapi import FastAPI
from loguru import logger

from config import settings, app
from api.images import router
from storage.redis import get_redis_pool
from db.db import Database, CONN_KWARGS
from db.tables import MediaBase

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
