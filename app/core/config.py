from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI Project"
    debug: bool = True
    db_type: str = "mongodb"
    database_url: str = "mongodb://localhost:27017/"   
    secret_key: str = "DAT_DEP_TRAI_QUA" 
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


    class Config:
        env_file = ".env"
    
settings = Settings()