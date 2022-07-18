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
        json=product.json(),
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
        offers = get_offers_by_product_id(product_id=product.id)
        offers_db = [
            Offer(product_id=product.id, date=date_time, **offer)
            for offer in offers
        ]
        offer_crud.delete_all_by_product_id(
            product_id=product.id, session=session
        )
        offer_crud.create_all(offers=offers_db, session=session)
    return True


def get_offers_by_product_id(product_id: int | None):
    response = requests.get(
        url=f"{settings.offer_url}/products/{product_id}/offers",
        headers={"Bearer": settings.offer_token},
    )
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Offer ms call error")
    return response.json()


def get_offers_loop():
    while True:
        get_offers(session=next(get_session()))
        time.sleep(settings.offer_refresh_rate_sec)
