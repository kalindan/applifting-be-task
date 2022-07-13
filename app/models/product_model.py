from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .offer_model import Offer


class ProductBase(SQLModel):
    name: str
    description: str


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    offers: list["Offer"] = Relationship(back_populates="product")


class ProductWrite(ProductBase):
    pass
