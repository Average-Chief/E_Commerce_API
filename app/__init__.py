from flask import Flask
from app.routes.auth import auth_bp
from app.routes.product import product_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)

    return app