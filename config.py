from pydantic import BaseSettings

class Settings(BaseSettings):
    api_key: str
    api_secret_key: str
    access_token: str
    access_token_secret: str

    class Config:
        env_file = ".env"

settings = Settings()