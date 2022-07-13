from email.policy import default

from sqlmodel import Field
from .offer_model import OfferBase
from .product_model import ProductBase


class OfferRead(OfferBase):
    pass


class ProductRead(ProductBase):
    id: int
    offers: list["OfferRead"] = []
