from app.models.product import Product
from sqlmodel import select

def getProductById(session, product_id:int):
        stmt = select(Product).where(Product.id == product_id)
        result = session.exec(stmt).first()
        return result