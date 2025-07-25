from fastapi import APIRouter
from app.api.v1.endpoints import users, restaurants

# This is the new, more explicit way to import the routers
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.restaurants import router as restaurants_router

api_router = APIRouter()

# We now use the imported router objects directly
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(restaurants_router, prefix="/restaurants", tags=["restaurants"])