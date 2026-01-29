from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    series: str = Field(nullable=False)
    author: str = Field(nullable=False)
    price_cents: int = Field(nullable=False, ge=0) # ge=0 means "greater than or equal to 0"
    stock: int = Field(default=0, ge=0) 
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


