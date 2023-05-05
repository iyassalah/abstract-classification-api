"""Entry point for the app, run this using uvicorn"""
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import batch, interactive
from .admin import admin
from .models import User
from .database import db

load_dotenv('../.env.dev')

app = FastAPI()

app.include_router(batch.router)
app.include_router(interactive.router)
app.include_router(admin.router)

#just to be able to send the request in the same machine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root_admin = User(username="root", email="root@example.com", password="password", isAdmin=True)

def create_root_admin():
    """
    Create a root admin user.

    Returns:
    - A dictionary containing the ID of the newly created user.
    """
    collection = db.users
    existing_user = collection.find_one({"username": "root"})
    if existing_user:
        print("Root admin user already exists.")
    else:
        root_admin_data = root_admin.dict()
        root_admin_data["isAdmin"] = True
        collection.insert_one(root_admin_data)

create_root_admin()

@app.get("/")
async def root():
    """
        root module
    """

    return {"message": "hi"}
