from app.models.cart import Cart, CartItem
from sqlmodel import select
from typing import Optional

def getCartbyUserId(session, user_id:int):
        stmt = select(Cart).where(Cart.user_id==user_id)
        result = session.exec(stmt).first()
        return result

def getCartItem(session, cart_id:int, product_id:int) -> Optional[CartItem]:
        stmt = select(CartItem).where(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id
        )
        cart_item = session.exec(stmt).first()
        return cart_item

