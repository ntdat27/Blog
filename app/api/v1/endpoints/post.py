from datetime import datetime, timedelta, timezone
from bson import ObjectId
import json
import redis
from app.core.config import settings
from fastapi import APIRouter, Depends, HTTPException , BackgroundTasks
from app.db.session import user_collection , post_collection , like_collection
from app.models.user import UserInDB 
from app.models.post import PostCreate , PostInDB
from app.db.session import post_collection , like_collection
from app.api.v1.endpoints.login import get_current_active_user
from fastapi.encoders import jsonable_encoder
from app.models.like import LikeCreate , LikeInDB
from app.services.producer import send_like_event
from app.api.v1.endpoints.email import send_mail
from app.models.email import EmailSchema
router = APIRouter()

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

@router.post("/posts/create")
def create_post(post: PostCreate, current_user : UserInDB = Depends(get_current_active_user)):
    post_in_db = PostInDB(
        title = post.title ,
        content = post.content, 
        author = current_user.email
    )
    post_dict = post_in_db.model_dump()
    post_collection.insert_one(post_dict)
    return {"message": "Create post"}

@router.post("/posts/{id}/update")
def update_post(id: str, post: PostCreate, background_tasks: BackgroundTasks, current_user : UserInDB = Depends(get_current_active_user)):
    post_collection.update_many(
        {"_id": ObjectId(id)},
        {"$set": {"title": post.title, "content": post.content}}
    )
    likes = like_collection.find({"post_id": id})
    emails_bao = [like["user_email"] for like in likes]
    if emails_bao:
        for mail_address in emails_bao:
            background_tasks.add_task(
                send_mail, EmailSchema(
                subject="Post Updated",
                body="Post ban vua thich vua duoc sua lai vao check di.",
                email=mail_address
            )
            )
    return {"message": "Update post"}   

@router.get("/posts/{id}")
def read_post(id: str):
    post_collection.update_one(
        {"_id": ObjectId(id)},
        {"$inc": {"view_count": 1}}
    )
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



@router.get("/posts/top/alltime")
def get_top_posts_view_all_time(current_user : UserInDB = Depends(get_current_active_user)):
    cached_data = redis_client.get("top_posts_all_time")
    if cached_data:
        print("CACHE HIT!")
        return json.loads(cached_data)
    print("CACHE MISS")
    view_all = post_collection.find().sort("view_count", -1).limit(10)
    result = []
    for post in view_all:
        post["_id"] = str(post["_id"])
        result.append(post)
    json_compatible_data = jsonable_encoder(result)
    redis_client.setex("top_posts_all_time", 300, json.dumps(json_compatible_data))
    print("cache have 5 minutes")
    return result

@router.get("/posts/top/today")
def get_top_posts_view_today(current_user : UserInDB = Depends(get_current_active_user)):
    today = datetime.now()
    start_time = today.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    end_time = today.replace(hour=23, minute=59, second=59, microsecond=999999, tzinfo=timezone.utc)
    view_today = post_collection.find({"created_at": {"$gte": start_time, "$lt": end_time}}).sort("view_count", -1).limit(10)
    result = []
    for post in view_today:
        post["_id"] = str(post["_id"])
        result.append(post)
    return result