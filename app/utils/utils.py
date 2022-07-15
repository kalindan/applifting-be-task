import time

import requests  # type:ignore
from fastapi import HTTPException
from sqlmodel import Session

from app.config import settings
from app.db import CRUDOffer, CRUDProduct, engine
from app.models import Offer, Product


async def register_product(product: Product) -> bool:
    response = requests.post(
        url=f"{settings.offer_url}/products/register",
        headers={"Bearer": settings.offer_token},
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
    if response.status_code == 201:
        return True
    raise HTTPException(status_code=500, detail="Offer ms call error")


def offer_caller():
    while True:
        with Session(engine) as session:
            products: list[Product] = CRUDProduct.read_all(session=session)
            for product in products:
                CRUDOffer.delete_all(product_id=product.id, session=session)
                offers = requests.get(
                    url=f"{settings.offer_url}/products/{product.id}/offers",
                    headers={"Bearer": settings.offer_token},
                ).json()
                for offer in offers:
                    offer_db = Offer(
                        id=offer["id"],
                        price=offer["price"],
                        items_in_stock=offer["items_in_stock"],
                        product_id=product.id,
                    )
                    CRUDOffer.create(offer=offer_db, session=session)
        time.sleep(60)
