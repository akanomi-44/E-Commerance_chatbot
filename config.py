import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess_secret_key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'hard_to_guess_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    MONGODB_SETTINGS = {
        'db': 'Store',
        'host': 'localhost',
        'port': 27017
    }
    APP_SECRET = os.getenv("APP_SECRET")
    FB_API_URL = os.getenv("FB_API_URL")
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
    PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
    PAGE_ID = os.getenv("PAGE_ID")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DB_USER_NAME = os.getenv("DB_USER_NAME")
    DB_PASS = os.getenv("DB_PASS")
    DB_CLUSTER = os.getenv("DB_CLUSTER")
