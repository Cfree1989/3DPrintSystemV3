from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from datetime import datetime, timedelta

def generate_confirmation_token(job_id: str, expires_hours: int = 168) -> tuple[str, datetime]:
    """
    Generate secure confirmation token with 7-day expiration
    
    Args:
        job_id: The job ID to generate token for
        expires_hours: Token expiration time in hours (default 168 = 7 days)
    
    Returns:
        tuple: (token_string, expiration_datetime)
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(job_id, salt='job-confirmation')
    expiration = datetime.utcnow() + timedelta(hours=expires_hours)
    return token, expiration

def confirm_token(token: str, max_age_hours: int = 168) -> str:
    """
    Validate confirmation token and return job ID
    
    Args:
        token: The token to validate
        max_age_hours: Maximum age in hours to accept (default 168 = 7 days)
    
    Returns:
        str: job_id if token is valid, None if invalid/expired
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        job_id = serializer.loads(
            token, 
            salt='job-confirmation', 
            max_age=max_age_hours * 3600
        )
        return job_id
    except Exception:
        return None  # Invalid/expired token 