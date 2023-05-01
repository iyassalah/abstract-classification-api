"""Entry point for the app, run this using uvicorn"""
# import logging
# import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from .routers import batch, interactive

load_dotenv('../.env.dev')

app = FastAPI()

app.include_router(batch.router)
app.include_router(interactive.router)

# set loguru format for root logger
# logging.getLogger().handlers = [InterceptHandler()]

# set format
# logger.configure(
#     handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}]
# )




# logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]

@app.get("/")
async def root():
    """TODO: add things here"""
    
    # logger.info("loguru log")
    # logging.info("logging log")
    # logger.add("./logs/logs.log")
    # logging.getLogger("fastapi").debug("fatapi info log")
    # logger.bind(payload=dict(request.query_params)).debug("params with formating")

    return {"message": "hi"}
