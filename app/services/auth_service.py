from app.utils.errors import UserAlreadyExists, InvalidCredentials, UserInactive, InvalidRefreshToken
from app.models.user import User
from app.extensions.db import engine, get_session
from app.extensions.jwt import generate_access_token
from app.utils.security import generate_refresh_token, hash_token, get_refresh_token_expiry
from app.storage.user_storage import getUserById, getUserByEmail
from app.models.refresh_token import RefreshToken
from app.config import settings
from passlib.hash import bcrypt
from sqlmodel import select
from datetime import datetime


def register_user(email:str, password:str)-> int:
    if getUserByEmail(email=email):
        raise UserAlreadyExists(f"User with email {email} already exists.")
    user = User(
        email=email, 
        password_hash=bcrypt.hash(password),
        role="USER",
        is_active=True
    )
    with get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user.id

def login_user(email:str, password:str)-> User:
    user = getUserByEmail(email=email)
    if not user:
        raise InvalidCredentials("Invalid email or password.")
    if user.is_active is False:
        raise UserInactive("User account is inactive.")
    if not bcrypt.verify(password, user.password_hash):
        raise InvalidCredentials("Invalid email or password.")
    with get_session() as session:
        existing_token = get_active_refresh_token(user.id)
        if existing_token:
            existing_token.revoked = True
            session.add(existing_token)
            session.commit()
    
    access_token = generate_access_token(user)
    raw_refresh_token = generate_refresh_token()
    hashed_refresh_token = hash_token(raw_refresh_token)

    refresh_token_obj = RefreshToken(
        user_id = user.id,
        token_hash = hashed_refresh_token,
        expires_at = get_refresh_token_expiry(),
    ) 

    session.add(refresh_token_obj)
    session.commit()

    return {
        "access_token": access_token,
        "refresh_token": raw_refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_SECONDS
    }
    
def get_active_refresh_token(user_id:int):
    stmt = select(RefreshToken).where(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked == True,
        RefreshToken.expires_at > datetime.utcnow()
    )
    with get_session() as session:
        return session.exec(stmt).first()

def refresh_access_token(refresh_token: str):
    hashed_token = hash_token(refresh_token)

    with get_session() as session:
        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == hashed_token,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        )
        existing_token = session.exec(stmt).first()

        if not existing_token:
            raise InvalidRefreshToken("Invalid or expired refresh token.")

        # Revoke old token
        existing_token.revoked = True
        session.add(existing_token)

        # Generate new refresh token
        new_raw_refresh_token = generate_refresh_token()
        new_hashed_refresh_token = hash_token(new_raw_refresh_token)

        new_refresh_token = RefreshToken(
            user_id=existing_token.user_id,
            token_hash=new_hashed_refresh_token,
            expires_at=get_refresh_token_expiry(),
        )

        session.add(new_refresh_token)

        # 🔥 Fetch user before generating access token
        user = getUserById(existing_token.user_id)
        access_token = generate_access_token(user)

        session.commit()

    return {
        "access_token": access_token,
        "refresh_token": new_raw_refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_SECONDS
    }


def logout_user(refresh_token:str):
    hashed_token = hash_token(refresh_token)
    with get_session() as session:
        stmt = select(RefreshToken).where(
            RefreshToken.token_hash==hashed_token,
            RefreshToken.revoked== False,
            RefreshToken.expires_at > datetime.utcnow()
        )
        existing_token = session.exec(stmt).first()
        if not existing_token:
            raise InvalidRefreshToken("Invalid or Expired refresh token.")
        
        existing_token.revoked=True
        session.add(existing_token)
        session.commit()