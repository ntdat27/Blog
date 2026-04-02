from datetime import timedelta
import token
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from app.core.security import create_access_token, verify_password, DUMMY_HASH, get_password_hash , create_refresh_token
from app.db.session import user_collection
from app.models.token import Token , TokenRefreshRequest
from app.models.user import UserInDB , UserCreate
from app.api.v1.endpoints.login import get_current_active_user
import jwt
router = APIRouter()

def authenticate_user(email: str, password: str):
    user_dict = user_collection.find_one({"email": email})
    if not user_dict:
        return False
    
    print(user_dict)
        
    user = UserInDB(**user_dict)
    if not verify_password(password, user.hashed_password):
        return False
    return user

@router.post("/register")
def register_user(user: UserCreate):
    if user_collection.find_one({"email": user.email}):
        return {"message": "Email da dang ki"}
    hashed_pw = get_password_hash(user.password)
    user_in_db = UserInDB(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw
    )
    user_dict = user_in_db.model_dump()
    user_collection.insert_one(user_dict)
    return {"message": "Dang Ky THanh Cng."}

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@router.post("/refresh", response_model=Token)
def refresh_access_token(request : TokenRefreshRequest):
    try:
        payload = jwt.decode(request.refresh_token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token không chứa email")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Sai invalid token: {str(e)}")
    
    user_dict = user_collection.find_one({"email": email})
    if user_dict is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)
    refresh_token = create_refresh_token(
        data={"sub": email}, expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@router.get("/me", response_model=UserInDB)
def read_users_me(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
):
    return current_user