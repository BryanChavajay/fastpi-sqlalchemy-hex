from fastapi import APIRouter

from app.routers.v1 import login, user
from app.config import API_V1_STR

api_router = APIRouter()

# API v1
api_router.include_router(login.router, prefix=f"{API_V1_STR}/login")
api_router.include_router(user.router, prefix=f"{API_V1_STR}/user")
