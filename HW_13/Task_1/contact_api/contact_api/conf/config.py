from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Завантаження змінних середовища з файлу .env
load_dotenv()

class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

settings = Settings(
    sqlalchemy_database_url=os.getenv("SQLALCHEMY_DATABASE_URL"),
    secret_key=os.getenv("SECRET_KEY"),
    algorithm=os.getenv("ALGORITHM"),
    mail_username=os.getenv("MAIL_USERNAME"),
    mail_password=os.getenv("MAIL_PASSWORD"),
    mail_from=os.getenv("MAIL_FROM"),
    mail_port=int(os.getenv("MAIL_PORT")),
    mail_server=os.getenv("MAIL_SERVER"),
    cloudinary_name=os.getenv("CLOUDINARY_NAME"),
    cloudinary_api_key=os.getenv("CLOUDINARY_API_KEY"),
    cloudinary_api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
