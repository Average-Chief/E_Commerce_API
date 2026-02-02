from functools import wraps
from flask import request
import jwt
from sqlmodel import select
from app.config import settings
from app.utils.errors import Unauthorized, Forbidden
from app.models.user import User
from app.extensions.db import get_session
from datetime import datetime

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise Unauthorized("Authorization header missing.")
        
        parts = auth_header.split(" ")
        if len(parts)!=2 or parts[0]!="Bearer":
            raise Unauthorized("Invalid authorization header format.")
        
        token = parts[1]
        try:
            payload= jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Access token Expired.")
        except jwt.InvalidTokenError:
            raise Unauthorized("Invalid Access token.")
        
        user_id = payload.get("sub")
        if not user_id:
            raise Unauthorized("Invalid access token payload.")
        
        with get_session() as session:
            stmt = select(User).where(
                User.id== int(user_id),
                User.is_active == True
            )
            user = session.exec(stmt).first()

        if not user:
            raise Unauthorized("User not found or inactive.")
        
        request.user = user

        return fn(*args,**kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    @auth_required
    def wrapper(*args,**kwargs):
        user = request.user
        if user.role.lower()!='admin':
            raise Forbidden("Admin access required.")
        
        return fn(*args, **kwargs)
    return wrapper