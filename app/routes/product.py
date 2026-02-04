from app.middleware.auth import admin_required
from flask import Blueprint, request, jsonify
from app.services.product_service import(
    create_product,
    update_product,
    update_product_stock,
    deactivate_product,
    get_product_by_id,
    list_products
)

product_bp = Blueprint("products",__name__,url_prefix="/products")

@product_bp.get("/")
def get_products():
    search = request.args.get("q")
    products = list_products(search)
    return jsonify([p.model_dump() for p in products]), 200

@product_bp.get("/<int:product_id>")
def get_product(product_id:int):
    product = get_product_by_id(product_id)
    return jsonify(product.model_dump()), 200

@product_bp.post("/")
@admin_required
def create_product_route():
    data = request.get_json()
    result = create_product(
        title = data["title"],
        series = data["series"],
        author = data["author"],
        price_cents = data["price_cents"],
        stock = data["stock"]
    )
    return jsonify({
        "message": "Product added successfully.",
        "product_id": result
    }), 201

@product_bp.patch("/<int:product_id>")
@admin_required
def update_product_route(product_id:int):
    data = request.get_json() or {}
    product = update_product(
        product_id = product_id,
        title = data.get("title"),
        author = data.get("author"),
        series = data.get("series"),
        price_cents = data.get("price_cents"),
    )
    return jsonify(product.model_dump()), 200

@product_bp.patch("/<int:product_id>/stock")
@admin_required
def update_product_stock_route(product_id:int):
    data = request.get_json()
    product = update_product_stock(
        product_id=product_id,
        stock = data["stock"]
    )
    return jsonify(product), 200

@product_bp.delete("/<int:product_id>")
@admin_required
def deactivate_product_route(product_id:int):
    product = deactivate_product(product_id)
    return jsonify(product), 204