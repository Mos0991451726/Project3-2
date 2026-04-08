from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "goldbot_db"
    JWT_SECRET: str = "change-this-secret"
    JWT_EXPIRE_HOURS: int = 24
    GEMINI_API_KEY: str = ""
    OLLAMA_HOST: str = "http://localhost:11434"
    CHROMA_PATH: str = "./chroma_db"
    CHROMA_COLLECTION: str = "gold_knowledge"
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

settings = Settings()
