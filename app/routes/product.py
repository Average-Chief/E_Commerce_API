from app.middleware.auth import admin_required
from flask import Blueprint, request, jsonify
from app.schemas.product import ProductResponse, CreateProductRequest, UpdateProductRequest, UpdateStockRequest
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
    response = [
        ProductResponse.model_validate(p).model_dump()
        for p in products
    ]
    return jsonify(response), 200

@product_bp.get("/<int:product_id>")
def get_product(product_id:int):
    product = get_product_by_id(product_id)
    response = ProductResponse.model_validate(product)
    return jsonify(response.model_dump()), 200

@product_bp.post("/")
@admin_required
def create_product_route():
    req = CreateProductRequest(**request.json)
    product_id = create_product(**req.model_dump())
    return jsonify({
        "message": "Product added successfully.",
        "product_id": product_id
    }), 201

@product_bp.patch("/<int:product_id>")
@admin_required
def update_product_route(product_id:int):
    req = UpdateProductRequest(**request.json)
    product = update_product(product_id, **req.model_dump(exclude_none=True))
    response = ProductResponse.model_validate(product)
    return jsonify(response.model_dump()), 200

@product_bp.patch("/<int:product_id>/stock")
@admin_required
def update_product_stock_route(product_id:int):
    req = UpdateStockRequest(**request.json)
    product = update_product_stock(product_id, req.stock)
    response = ProductResponse.model_validate(product)
    return jsonify(response), 200

@product_bp.delete("/<int:product_id>")
@admin_required
def deactivate_product_route(product_id:int):
    product = deactivate_product(product_id)
    return jsonify({
        "message": "Product deactivated successfully"
    }), 204