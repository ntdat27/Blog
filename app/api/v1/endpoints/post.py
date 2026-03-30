from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from app.db.session import user_collection , post_collection , like_collection
from app.models.user import UserInDB 
from app.models.post import PostCreate , PostInDB
from app.db.session import post_collection , like_collection
from app.api.v1.endpoints.login import get_current_active_user
from app.models.like import LikeCreate , LikeInDB
from app.services.producer import send_like_event
router = APIRouter()

@router.post("/posts/create")
def create_post(post: PostCreate, current_user : UserInDB = Depends(get_current_active_user)):
    post_in_db = PostInDB(
        title = post.title ,
        content = post.content, 
        author = current_user.email
    )
    post_dict = post.model_dump()
    post_collection.insert_one(post_dict)
    return {"message": "Create post"}

@router.get("/posts/{id}")
def read_post(id: str):
    post = post_collection.find_one({"_id":ObjectId(id)})
    if post:
        post["_id"] = str(post["_id"])
        return post
    return {"message": "Post not found"}

@router.post("/posts/{id}/like")
def like_post(id: str, current_user : UserInDB = Depends(get_current_active_user)):
    if not post_collection.find_one({"_id": ObjectId(id)}):
        return {"message": "Post not found"}
    existing_like = like_collection.find_one({"post_id": id, "user_email": current_user.email})
    if existing_like:
        like_collection.delete_one({"_id": existing_like["_id"]})
        send_like_event(post_id=id, user_email=current_user.email, action="decrease")
        return{"message":"Da bo thich bai viet"}
    else:
        new_like = LikeInDB(
            user_email=current_user.email,
            post_id=id
        )
        like_collection.insert_one(new_like.model_dump())
        send_like_event(post_id=id, user_email=current_user.email, action="increase")   
    return {"message": "Da thich bai viet"}



