from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, ForeignKey

class Order(SQLModel, table=True):
    __tablename__ = "orders"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        sa_column=Column(
            ForeignKey("users.id"),
            nullable = False
        )
    )
    total_amount_cents: int = Field(nullable=False, ge=0)
    status: str 
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OrderItems(SQLModel, table=True):
    __tablename__ = "order_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(
        sa_column=Column(
            ForeignKey("orders.id"),
            nullable=False
        )
    )
    product_id: int = Field(
        sa_column=Column(
            ForeignKey("products.id"),
            nullable=True
        )
    )
    title_snapshot: str
    price_snapshot: int = Field(nullable=False, ge=0)
    quantity: int = Field(nullable = False, ge=1)
