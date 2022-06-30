import aiohttp
from loguru import logger


async def fetch_image(url, session):
    async with session.get(url, allow_redirects=True) as response:
        logger.info(f'Trying to fetch image from url: {url}')
        return await response.read()


async def create_session(url):
    async with aiohttp.ClientSession() as session:
        return await fetch_image(url, session)
