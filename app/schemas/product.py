from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ProductResponse(BaseModel):
    id: int
    title: str
    series: str
    author: str
    price_cents: int = Field(ge=0)
    stock: int = Field(ge=0)
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CreateProductRequest(BaseModel):
    title: str
    series: str
    author: str
    price_cents: int = Field(ge=0)
    stock: int = Field(ge=0)

class UpdateProductRequest(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    series: Optional[str] = None
    price_cents: Optional[int] = Field(ge=0)

class UpdateStockRequest(BaseModel):
    stock: int = Field(ge=0)