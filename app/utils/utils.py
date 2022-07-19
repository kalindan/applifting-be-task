import asyncio
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Coroutine

from fastapi import HTTPException
from httpx import AsyncClient

from app.config import settings
from app.crud import offer_crud, product_crud
from app.db import async_session
from app.models import Offer, Product


async def register_product(product: Product) -> bool:
    async with AsyncClient() as client:
        response = await client.post(
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


async def get_offers() -> bool:
    async with async_session() as session:
        products: list[Product] | None = await product_crud.read_all(
            session=session
        )
    if not products:
        return False
    product_offers = await asyncio.gather(
        *[
            get_offers_by_product_id(product_id=product.id)
            for product in products
        ]
    )

    return True


async def get_offers_by_product_id(product_id: int | None) -> bool:
    async with AsyncClient() as client:
        response = await client.get(
            url=f"{settings.offer_url}/products/{product_id}/offers",
            headers={"Bearer": settings.offer_token},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Offer ms call error")
    async with async_session() as session:
        await offer_crud.delete_all_by_product_id(
            product_id=product_id, session=session
        )
        offers = response.json()
        date_time = datetime.now()
        await offer_crud.create_all(
            offers=[
                Offer(product_id=product_id, date=date_time, **offer)
                for offer in offers
            ],
            session=session,
        )
    return True


def repeat_every(
    *,
    seconds: int,
) -> Callable[
    [Callable[[], Coroutine[Any, Any, None]]],
    Callable[[], Coroutine[Any, Any, None]],
]:
    def decorator(
        func: Callable[[], Coroutine[Any, Any, None]]
    ) -> Callable[[], Coroutine[Any, Any, None]]:
        @wraps(func)
        async def wrapped() -> None:
            async def loop() -> None:
                while True:
                    await func()
                    await asyncio.sleep(seconds)

            asyncio.ensure_future(loop())

        return wrapped

    return decorator


@repeat_every(seconds=settings.offer_refresh_rate_sec)
async def get_offers_task():
    await get_offers()
