import time
from datetime import datetime

import requests  # type:ignore
from fastapi import HTTPException
from sqlmodel import Session

from app.config import settings
from app.crud import offer_crud, product_crud
from app.db import get_session
from app.models import Offer, Product


def register_product(product: Product) -> bool:
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


def get_offers(session: Session) -> bool:
    products: list[Product] = product_crud.read_all(session=session)
    date_time = datetime.now()
    for product in products:
        response = requests.get(
            url=f"{settings.offer_url}/products/{product.id}/offers",
            headers={"Bearer": settings.offer_token},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Offer ms call error")
        offer_crud.delete_all(product_id=product.id, session=session)
        offers = response.json()
        for offer in offers:
            offer_db = Offer(
                id=offer["id"],
                price=offer["price"],
                items_in_stock=offer["items_in_stock"],
                product_id=product.id,
            )
            offer_db.date = date_time
            offer_crud.create(offer=offer_db, session=session)
    return True


def get_offers_loop():
    while True:
        get_offers(session=next(get_session()))
        time.sleep(60)


def register_product_and_get_offers():
    pass
