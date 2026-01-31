import secrets 
import hashlib
from datetime import datetime, timedelta
from app.config import settings

def generate_refresh_token()->str:
    return secrets.token_urlsafe(64)

def hash_token(token:str)-> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def get_refresh_token_expiry():
    return datetime.utcnow() + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS)
