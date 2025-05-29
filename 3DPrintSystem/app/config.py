import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
 
class Config:
    # Flask Core Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL environment variable is required")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Storage Configuration
    APP_STORAGE_ROOT = os.environ.get('STORAGE_PATH', 'storage')
    UPLOAD_FOLDER = os.path.join(APP_STORAGE_ROOT, 'Uploaded')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Application Configuration
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
    
    # Staff Authentication
    STAFF_PASSWORD = os.environ.get('STAFF_PASSWORD')
    if not STAFF_PASSWORD:
        raise ValueError("STAFF_PASSWORD environment variable is required")
    
    # Optional: Task Queue Configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    
    @classmethod
    def validate_required_config(cls):
        """Validate that all required configuration is present"""
        required_vars = ['SECRET_KEY', 'DATABASE_URL', 'STAFF_PASSWORD']
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Validate email configuration if any email vars are set
        email_vars = ['MAIL_SERVER', 'MAIL_USERNAME', 'MAIL_PASSWORD', 'MAIL_DEFAULT_SENDER']
        email_vars_set = [var for var in email_vars if os.environ.get(var)]
        
        if email_vars_set and len(email_vars_set) != len(email_vars):
            missing_email_vars = [var for var in email_vars if not os.environ.get(var)]
            print(f"Warning: Incomplete email configuration. Missing: {', '.join(missing_email_vars)}")
        
        return True 