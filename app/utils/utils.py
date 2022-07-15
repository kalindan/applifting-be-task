import time

import requests  # type:ignore
from fastapi import HTTPException
from requests import Response
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


def get_offers():
    while True:
        with Session(engine) as session:
            products: list[Product] = CRUDProduct.read_all(session=session)
            for product in products:
                response: Response = requests.get(
                    url=f"{settings.offer_url}/products/{product.id}/offers",
                    headers={"Bearer": settings.offer_token},
                )
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=500, detail="Offer ms call error"
                    )
                offers = response.json()
                for offer in offers:
                    offer_db = CRUDOffer.read_by_id(
                        id=offer["id"], session=session
                    )
                    if not offer_db:
                        offer_db = Offer(
                            id=offer["id"],
                            price=offer["price"],
                            items_in_stock=offer["items_in_stock"],
                            product_id=product.id,
                        )
                        CRUDOffer.create(offer=offer_db, session=session)
                    else:
                        offer_db.price = offer["price"]
                        offer_db.items_in_stock = offer["items_in_stock"]
                        CRUDOffer.update(offer=offer_db, session=session)
        time.sleep(60)
