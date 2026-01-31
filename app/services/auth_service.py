from app.utils.errors import UserAlreadyExists, InvalidCredentials, UserInactive, InvalidRefreshToken
from app.models.user import User
from app.storage.user_storage import addUser, getUserByEmail
from app.models.refresh_token import RefreshToken
from passlib.hash import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


def register_user(email:str, password:str)-> User:
    if User.exists(email=email):
        raise UserAlreadyExists(f"User with email {email} already exists.")
    user = User(
        email=email, 
        password_hash=bcrypt.hash(password),
        role="USER",
        is_active=True
    )
    addUser(user)
    return user.id

def login_user(email:str, password:str)-> User:
    user = getUserByEmail(email=email)
    if not user:
        raise InvalidCredentials("Invalid email or password.")
    if user.is_active is False:
        raise UserInactive("User account is inactive.")
    if not bcrypt.verify(password, user.password_hash):
        raise InvalidCredentials("Invalid email or password.")
    