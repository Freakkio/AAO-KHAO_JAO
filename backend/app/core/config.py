import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_DETAILS: str = os.getenv("MONGO_DETAILS")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


settings = Settings()