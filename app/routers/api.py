from fastapi import APIRouter
from app.routers import users

router = APIRouter()

def include_api_routes():
  router.include_router(users.router)

include_api_routes()