from typing import List, Optional
import sqlalchemy as SA
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    products: Mapped[List["Product"]] = relationship(back_populates="user")

    


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(SA.ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="products")

    __table_args__ = (SA.UniqueConstraint("name", "user_id", name="_user_product_uc"),)

