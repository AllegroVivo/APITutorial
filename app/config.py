from pydantic_settings import BaseSettings
from dotenv import load_dotenv
################################################################################
class Settings(BaseSettings):

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    class Config:
        env_file = ".env"
    
################################################################################

load_dotenv()
settings = Settings()

################################################################################
