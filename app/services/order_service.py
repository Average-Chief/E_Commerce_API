from app.models.order import OrderItems, Order
from app.models.product import Product
from app.storage.cart_storage import getAllItems
from app.extensions.db import get_session
from app.utils.errors import (
    ProductInactive,
    ProductNotFound,
    InsufficientStock,
    EmptyCartError
)
from app.services.cart_service import get_or_create_cart
from sqlmodel import select
from datetime import datetime

def create_order_from_cart(user_id:int):
    with get_session() as session:
        cart = get_or_create_cart(session, user_id)
        cart_items = getAllItems(session, cart.id)
        if not cart_items:
            raise EmptyCartError("The cart is empty.")
        
        total_amount = 0
        # validate products and stock first
        validated_products = []

        for item in cart_items:
            stmt = select(Product).where(Product.id==item.product_id)
            product = session.exec(stmt).first()

            if not product:
                raise ProductNotFound("Product not found.")
            if not product.is_active:
                raise ProductInactive("Product is inactive.")
            if item.quantity>product.stock:
                raise InsufficientStock("Not enough stock available.")
            validated_products.append([item, product])
        
        #create_order
        order = Order(
            user_id=user_id,
            total_amount_cents=0,
            status="PENDING",
            created_at=datetime.utcnow()
        )
        session.add(order)
        session.flush()

        for item, product in validated_products:
            subtotal = product.price_cents * item.quantity
            total_amount += subtotal
            
            order_item = OrderItems(
                order_id = order.id,
                product_id= product.id,
                title_snapshot=product.title,
                price_snapshot=product.price_cents,
                quantity=item.quantity
            )
            session.add(order_item)
        
        order.total_amount_cents = total_amount
        session.add(order)
        session.commit()
        session.refresh(order)

        return order.id




    