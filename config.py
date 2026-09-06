import os
import secrets
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('PRIMARY_SECRET_KEY') or secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = os.getenv('PRIMARY_DATABASE_URI', 'sqlite:///jobboard.db')
    API_KEY = os.getenv('PRIMARY_API_KEY')

    SQLALCHEMY_TRACK_MODIFICATIONS = False