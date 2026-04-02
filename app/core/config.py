import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI Project"
    debug: bool = True
    db_type: str = "mongodb"
    database_url: str = "mongodb://localhost:27017/"   
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "DAT_DEP_TRAI_QUA" 
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    smtp_host: str = "sandbox.smtp.mailtrap.io"
    smtp_port: int = 2525
    smtp_user: str = "67edb38dcbd53a"
    smtp_pass: str = "62965c6a7b83a3"
    mailtraptoken: str = "0b27180095cff0eb94571e0ea7d7d993"
    class Config:
        env_file = ".env"
        extra = "ignore"
    
settings = Settings()