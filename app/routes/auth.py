from app.middleware.auth import auth_required
from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user, refresh_access_token, logout_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/signup")
def signup():
    data = request.get_json()
    results = register_user(
        email=data["email"],
        password=data["password"]
    )
    return jsonify({
        "message": "User registered successfully",
        "user_id": results
    }), 201

@auth_bp.post("/login")
def login():
    data = request.get_json()
    result = login_user(
        email = data["email"],
        password = data["password"]
    )
    return jsonify(result), 200

@auth_bp.post("/refresh")
def refresh():
    data = request.get_json()
    result = refresh_access_token(
        data["refresh_token"]
    )
    return jsonify(result), 200

@auth_bp.post("/logout")
@auth_required
def logout():
    data = request.get_json()
    result = login_user(data["refresh_token"])
    return jsonify({"message": "Logged out successfully"}), 200

