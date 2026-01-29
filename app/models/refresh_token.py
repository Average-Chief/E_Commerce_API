from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import Column, ForeignKey
from datetime import datetime

class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        sa_column= Column(
            ForeignKey("users.id"),
            nullable=False
        )
    )
    token_hash: str = Field(nullable=False, unique=True)
    expires_at: datetime = Field(nullable=False)
    revoked: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    