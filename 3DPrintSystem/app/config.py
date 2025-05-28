import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
 
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # Add a real secret key to .env
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///app.db' # Default to SQLite if DATABASE_URL is not set
    SQLALCHEMY_TRACK_MODIFICATIONS = False 