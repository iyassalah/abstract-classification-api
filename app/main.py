"""Entry point for the app, run this using uvicorn"""
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import batch, interactive
from .admin import admin, create_root_admin
from .database import setup_db_indexes

load_dotenv("../.env.dev")

app = FastAPI()

app.include_router(batch.router)
app.include_router(interactive.router)
app.include_router(admin.router)

# just to be able to send the request in the same machine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


create_root_admin()
setup_db_indexes()


@app.get("/")
async def root():
    """
    root module
    """

    return {"message": "hi"}
