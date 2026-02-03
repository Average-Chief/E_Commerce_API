from app.models.product import Product
from datetime import datetime
from app.utils.errors import InvalidStockValue, ProductInactive, ProductNotFound, InvalidProductData
from sqlmodel import select
from app.extensions.db import get_session
from app.storage.product_storage import getProductById

def create_product(title:str, series:str, author:str, price_cents:int, stock:int):
    if price_cents<0:
        raise InvalidProductData("Price cannot be less than zero.")
    if stock<0:
        raise InvalidStockValue("Stock cannot go less than zero.")
    
    with get_session() as session:
        new_product = Product(
            title = title,
            series = series,
            author = author,
            price_cents=price_cents,
            stock = stock,
            is_active = True,
            created_at = datetime.utcnow(),
        )
        session.add(new_product)
        session.commit()
        session.refresh(new_product)

    return {
        "message": "Product added Successfully",
        "product_id": new_product.id
    }

def update_product(
    product_id: int,
    title: str | None = None,
    author: str | None = None,
    series: str | None = None,
    price_cents: int | None = None,
):
    with get_session() as session:
        product = getProductById(session, product_id)
        if not product:
            raise ProductNotFound("Product not found.")
        if not product.is_active:
            raise ProductInactive("Cannot update in-active product.")
    
        if title is not None:
            product.title = title
        if author is not None:
            product.author= author
        if series is not None:
            product.series= series
        if price_cents is not None:
            if price_cents<0:
                raise InvalidProductData("Price cannot be less than zero.")
            product.price_cents= price_cents
    
        session.add(product)
        session.commit()
        session.refresh(product)

        return product

def update_product_stock(product_id:int, stock:int):
    with get_session() as session:
        product = getProductById(session, product_id)
        if not product:
            raise ProductNotFound("Product not found.")
        if stock<0:
            raise InvalidStockValue("Stock cannot go less than zero.")
        
        product.stock=stock
        session.add(product)
        session.commit()
        session.refresh(product)

        return {
            "message": "Stock updated.",
            "stock": product.stock
        }


    

    
    
    



    