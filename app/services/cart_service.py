from app.models.cart import Cart, CartItem
from app.models.product import Product
from sqlmodel import select
from datetime import datetime
from app.extensions.db import get_session
from app.storage.product_storage import getProductById
from app.storage.user_storage import getUserById
from app.storage.cart_storage import getCartbyUserId, getCartItem, getAllItems
from app.utils.errors import (
    UserInactive, 
    UserNotFound, 
    ProductInactive, 
    ProductNotFound, 
    InvalidQuantity, 
    InsufficientStock,
    CartItemNotFound
)

def get_or_create_cart(session, user_id: int):
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

def add_to_cart(user_id:int, product_id:int, quantity:int):
    if quantity<=0:
        raise InvalidQuantity("Quantity should be greater than zero.")
    with get_session() as session:
        product = getProductById(session, product_id)
        if not product:
            raise ProductNotFound("Product not found.")
        if not product.is_active:
            raise ProductInactive("Cannot update in-active product.")
        if product.stock<quantity:
            raise InsufficientStock("Not enough stock available.")
        
        cart = get_or_create_cart(session, user_id)
        cart_item = getCartItem(session, cart.id, product.id)
        if cart_item:
            new_quantity = cart_item.quantity + quantity

            if new_quantity > product.stock:
                raise InsufficientStock("Not enough stock available.")
            cart_item.quantity = new_quantity
        
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity
            )
            session.add(cart_item)
        
        cart.updated_at= datetime.utcnow()
        session.add(cart)
        session.commit()
        session.refresh(cart)

        return cart

def update_cart_item(user_id:int, product_id:int, quantity:int):
    if quantity<0:
        raise InvalidQuantity("Quantity should be greater than zero.")
    with get_session() as session:
        cart = get_or_create_cart(session, user_id)
        cart_item = getCartItem(session, cart.id, product_id)
        if not cart_item:
            raise CartItemNotFound("Item not found in cart.")
        
        if quantity==0:
            session.delete(cart_item)
            cart.updated_at = datetime.utcnow()
            session.add(cart)
            session.commit()
            return cart
        
        product = getProductById(session,product_id)
        if not product:
            raise ProductNotFound("Product not found.")
        if not product.is_active:
            raise ProductInactive("Product is inactive.")
        if quantity>product.stock:
            raise InsufficientStock("Not enough stock available.")
        
        cart_item.quantity = quantity
        session.add(cart_item)
        cart.updated_at = datetime.utcnow()
        session.add(cart)
        session.commit()
        session.refresh(cart)
        return cart
    
def remove_from_cart(user_id:int, product_id:int):
    with get_session() as session:
        cart = get_or_create_cart(session, user_id)
        item = getCartItem(session, cart.id, product_id)
        if not item:
            raise CartItemNotFound("Item not found in cart.")
        session.delete(item)
        cart.updated_at = datetime.utcnow()
        session.add(cart)
        session.commit()
        return cart

def get_cart(user_id:int):
    with get_session() as session:
        cart = get_or_create_cart(session, user_id)
        cart_items = getAllItems(session, cart.id)
        response_items = []
        total_cents = 0

        for item in cart_items:
            stmt = select(Product).where(Product.id == item.product_id)
            product = session.exec(stmt).first()

            if not product or not product.is_active:
                continue

            subtotal = product.price_cents * item.quantity 
            total_cents+= subtotal

            response_items.append({
                "product_id":product.id,
                "title":product.title,
                "price_cents":product.price_cents,
                "quantity":item.quantity,
                "subtotal_cents": subtotal
            })

        return {
            "cart_id": cart.id,
            "items": response_items,
            "total_cents": total_cents
        }

def clear_cart(user_id:int):
    with get_session() as session:
        cart = get_or_create_cart(session, user_id)
        cart_items = getAllItems(session, cart.id)
        for item in cart_items:
            session.delete(item)
        cart.updated_at = datetime.utcnow()
        session.add(cart)
        session.commit()

