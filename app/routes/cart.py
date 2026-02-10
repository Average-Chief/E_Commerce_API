from app.services.cart_service import (
    add_to_cart,
    get_cart,
    remove_from_cart,
    clear_cart,
    update_cart_item
)
from flask import Blueprint, request, jsonify, g
from app.middleware.auth import auth_required

cart_bp  = Blueprint("cart",__name__, url_prefix="/cart")

@cart_bp.get("/")
@auth_required
def get_cart_route():
    cart = get_cart(g.user.id)
    return jsonify(cart), 200

@cart_bp.post("/items")
@auth_required
def add_item_to_cart_route():
    data = request.get_json() or {}
    cart = add_to_cart(g.user.id, data["product_id"], data["quantity"])
    return jsonify(cart), 201

@cart_bp.patch("/items/<int:product_id>")
@auth_required
def update_cart_item_route(product_id:int):
    data = request.get_json() or {}
    cart = update_cart_item(g.user.id, product_id, data["quantity"])
    return jsonify({
        "message": "Cart Updated",
        "updated_cart": cart
    }), 200

@cart_bp.delete("/items/<int:product_id>")
@auth_required
def remove_item_from_cart_route(product_id:int):
    cart = remove_from_cart(g.user.id, product_id)
    return jsonify(cart), 200

@cart_bp.delete("/clear")
@auth_required
def clear_cart_route():
    clear_cart(g.user.id)
    return jsonify ({
        "message":"Cart is Empty"
    }), 200