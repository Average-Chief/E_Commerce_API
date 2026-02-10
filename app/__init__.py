from flask import Flask
from sqlmodel import SQLModel
from app.extensions.db import engine
from app.models import *
from app.routes.auth import auth_bp
from app.routes.product import product_bp
from app.routes.cart import cart_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)

    SQLModel.metadata.create_all(engine)

    return app