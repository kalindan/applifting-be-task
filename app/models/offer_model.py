from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .product_model import Product


class OfferBase(SQLModel):
    price: int
    items_in_stock: int


class Offer(OfferBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int | None = Field(default=None, foreign_key="product.id")
    product: "Product" = Relationship(back_populates="offers")


class OfferWrite(OfferBase):
    product_id: int
