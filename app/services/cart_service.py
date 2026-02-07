from app.models.cart import Cart, CartItem
from sqlmodel import select
from app.extensions.db import get_session
from app.storage.user_storage import getUserById
from app.storage.cart_storage import getCartbyUserId
from app.utils.errors import UserInactive, UserNotFound

def get_or_create_cart(user_id: int):
    with get_session() as session:
        user = getUserById(session, user_id)
        if not user:
            raise UserNotFound("User not found.")
        if not user.is_active:
            raise UserInactive("User account is inactive.")

        cart = getCartbyUserId(session, user_id)
        if cart:
            return cart

        new_cart = Cart(user_id=user_id)
        session.add(new_cart)
        session.commit()
        session.refresh(new_cart)
        return new_cart

