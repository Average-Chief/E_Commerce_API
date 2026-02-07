from app.models.cart import Cart
from sqlmodel import select, Session
from app.extensions.db import engine

def getCartbyUserId(session, user_id:int):
        stmt = select(Cart).where(Cart.user_id==user_id)
        result = session.exec(stmt).first()
        return result