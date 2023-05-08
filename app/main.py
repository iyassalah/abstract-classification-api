"""Entry point for the app, run this using uvicorn"""
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import batch, interactive
from .admin import admin, create_root_admin
from .database import setup_db_indexes


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

@app.on_event('startup')
async def startup_event():
    """load the configs here"""
    setup_db_indexes()
    load_dotenv("../.env.dev", verbose=True)
    create_root_admin()


@app.get("/")
async def root():
    """
    root module
    """

    return {"message": "hi"}
