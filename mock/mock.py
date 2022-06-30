import asyncio
from fastapi import FastAPI, responses

app = FastAPI()


@app.get("/")
async def get_body():
    # await asyncio.sleep(30)
    return responses.FileResponse("elephant.jpg")
