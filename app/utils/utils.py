import time
from fastapi import HTTPException
import requests  # type:ignore
from sqlmodel import Session
from app.config.config import config
from app.db.database import engine
from app.db.crud import CRUDOffer, CRUDProduct
from app.models.product_model import Product
from app.models.offer_model import Offer


async def register_product(product: Product):
    response = requests.post(
        url=f"{config.offer_url}/products/register",
        headers={"Bearer": config.offer_token},
        json={
            "id": product.id,
            "name": product.name,
            "description": product.description,
        },
    )
    if response.status_code == 400:
        raise HTTPException(status_code=400, detail="Bad request")
    if response.status_code == 406:
        raise HTTPException(status_code=406, detail="Unauthorized")
    return


def offer_caller():
    while True:
        with Session(engine) as session:
            products: list[Product] = CRUDProduct.read_all(session=session)
            for product in products:
                response = requests.get(
                    url=f"{config.offer_url}/products/{product.id}/offers",
                    headers={"Bearer": config.offer_token},
                )
                offer = response.json()[-1]
                offer_db = Offer(
                    price=offer["price"],
                    items_in_stock=offer["items_in_stock"],
                    product_id=product.id,
                )
                CRUDOffer.create(offer=offer_db, session=session)
                print(offer_db.json())
        time.sleep(60)
