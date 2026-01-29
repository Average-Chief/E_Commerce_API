from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import Column, ForeignKey, UniqueConstraint, DateTime
from datetime import datetime

class Cart(SQLModel, table=True):
    __tablename__ = "carts"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        sa_column=Column(
            ForeignKey("users.id"),
            nullable=False,
            unique=True
        )
    )
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CartItem(SQLModel, table=True):
    __tablename__ = "cart_items"
    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uix_cart_product"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int = Field(
        sa_column=Column(
            ForeignKey("carts.id"),
            nullable = False
        )
    )
    product_id: int = Field(
        sa_column=Column(
            ForeignKey("products.id"),
            nullable = False
        )
    )
    quantity: int = Field(default=1, ge=1)

