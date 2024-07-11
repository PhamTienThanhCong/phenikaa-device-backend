from fastapi import APIRouter
from app.routers import users, auth, customers

router = APIRouter()

def include_api_routes():
  router.include_router(customers.router)
  router.include_router(users.router)
  router.include_router(auth.router)

include_api_routes()