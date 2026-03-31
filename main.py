
from fastapi import FastAPI
from app.db.session import db ,user_collection
from app.models.user import UserCreate
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.post import router as post_router
from app.api.v1.endpoints import auth
app = FastAPI(title="BLog cua toi")

db_users = []

app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(post_router, prefix="/api/v1", tags=["posts"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
