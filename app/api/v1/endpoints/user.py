from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from app.db.session import user_collection
from app.models.user import UserCreate

router = APIRouter()

db_users = []

@router.get("/")
def read_root():
    return {"message": "Blog ca nhan"}


@router.get("/users/all")
def read_all_users():
    users = []
    for user in user_collection.find():
        user["_id"] = str(user["_id"]) 
        users.append(user)
    return users

@router.get("/users/{id}")
def read_user(id: str):
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    return {"message": "User not found"}


@router.put("/users/{id}")
def update_user(id: str, user: UserCreate):
    user_dict = user.model_dump()
    result = user_collection.replace_one({"_id": ObjectId(id)}, user_dict)
    if result.matched_count > 0:
        return {"message": "User updated successfully"}
    return {"message": "User not found"}

@router.delete("/users/{id}")
def delete_user(id: str):
    xoa = user_collection.delete_one({"_id": ObjectId(id)})
    if xoa.deleted_count > 0:
        return {"message": "User deleted successfully"}