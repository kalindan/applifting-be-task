from .offer_model import OfferBase
from .product_model import ProductBase


class OfferRead(OfferBase):
    id: int


class ProductRead(ProductBase):
    id: int
    offers: list["OfferRead"] = []
