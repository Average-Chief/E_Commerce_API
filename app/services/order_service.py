from app.models.order import OrderItems, Order
from app.models.product import Product
from app.storage.cart_storage import getAllItems
from app.extensions.db import get_session
from app.utils.errors import (
    OrderCannotBeCancelled,
    OrderAlreadyProcessed,
    ProductInactive,
    ProductNotFound,
    InsufficientStock,
    EmptyCartError,
    OrderNotFound,
    Unauthorized
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

def get_order_by_id(order_id:int, user_id:int):
    with get_session() as session:
        stmt = select(Order).where(Order.id==order_id, Order.user_id==user_id)
        order = session.exec(stmt).first()
        if not order:
            raise OrderNotFound("Order not found.")
        if order.user_id != user_id:
            raise Unauthorized("You do not have permission to view this order.")
        
        stmt = select(OrderItems).where(OrderItems.order_id==order.id)
        items = session.exec(stmt).all()
        order_items = []
        total = 0

        for item in items:
            subtotal = item.price_snapshot * item.quantity
            total += subtotal
            order_items.append({
                "product_id": item.product_id,
                "title": item.title_snapshot,
                "price_cents": item.price_snapshot,
                "quantity": item.quantity,
                "subtotal_cents": subtotal
            })
        
        return {
            "order_id": order.id,
            "status": order.status,
            "total_amount_cents": order.total_amount_cents,
            "items": order_items
        }
    
def list_user_orders(user_id:int):
    with get_session() as session:
        stmt = select(Order).where(Order.user_id==user_id).order_by(Order.created_at.desc())
        orders = session.exec(stmt).all()
        result = []
        for order in orders:
            result.append({
                "order_id": order.id,
                "status": order.status,
                "total_cents": order.total_amount_cents,
                "created_at": order.created_at
            })
        return result

def mark_order_paid(order_id:int, user_id:int):
    with get_session() as session:
        stmt = select(Order).where(Order.id==order_id, Order.user_id==user_id)
        order = session.exec(stmt).first()
        if not order:
            raise OrderNotFound("Order not found.")
        if order.status != "PENDING":
            raise OrderAlreadyProcessed("Order has already been processed.")
        
        stmt = select(OrderItems).where(OrderItems.order_id==order.id)
        items = session.exec(stmt).all()
        for item in items:
            stmt = select(Product).where(Product.id==item.product_id)
            product = session.exec(stmt).first()
            if not product or product.stock < item.quantity:
                raise InsufficientStock("Not enough stock available to complete the order.")
            product.stock -= item.quantity
            session.add(product)
        
        order.status = "PAID"
        session.add(order)

        cart = get_or_create_cart(session, user_id)
        cart_items = getAllItems(session, cart.id)
        for ci in cart_items:
            session.delete(ci)
        session.commit()
        return order.id

def cancel_order(order_id:int, user_id:int):
    with get_session() as session:
        stmt = select(Order).where(Order.id==order_id, Order.user_id==user_id)
        order = session.exec(stmt).first()
        if not order:
            raise OrderNotFound("Order not found.")
        if order.status != "PENDING":
            raise OrderCannotBeCancelled("Only pending orders can be cancelled.")
        
        order.status = "CANCELLED"
        session.add(order)
        session.commit()
        return order.id
    