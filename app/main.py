"""Entry point for the app, run this using uvicorn"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .admin import admin, create_root_admin
from .database import setup_db_indexes
from .routers import auth, batch, interactive, classes
from .crud import populate_classes

app = FastAPI(swagger_ui_parameters={"displayRequestDuration": True})

app.include_router(batch.router)
app.include_router(interactive.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(classes.router)


# just to be able to send the request in the same machine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """load the configs, configure the DB"""
    setup_db_indexes()
    create_root_admin()
    populate_classes()


@app.get("/")
async def root():
    """
    root module
    """

    return {"message": "hi"}