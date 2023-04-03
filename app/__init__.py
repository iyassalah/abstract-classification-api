"""Root package"""
from fastapi import FastAPI
from .dependancies import *
from .models import *
from .routers import *

app = FastAPI()
