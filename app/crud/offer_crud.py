import asyncio

from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Offer


async def create(offer: Offer, session: AsyncSession) -> Offer:
    session.add(offer)
    await session.commit()
    await session.refresh(offer)
    return offer


async def create_all(offers: list[Offer], session: AsyncSession):
    for offer in offers:
        session.add(offer)
    await session.commit()
    return


async def read_by_id(id: int, session: AsyncSession) -> Offer | None:
    result = await session.execute(select(Offer).where(Offer.id == id))
    offer = result.scalars().first()
    if not offer:
        return None
    return offer


async def update(offer: Offer, session: AsyncSession) -> Offer:
    session.add(offer)
    await session.commit()
    await session.refresh(offer)
    return offer


async def delete_all_by_product_id(product_id, session: AsyncSession):
    result = await session.execute(
        select(Offer).where(Offer.product_id == product_id)
    )
    offers = result.scalars().all()
    await asyncio.gather(*[session.delete(offer) for offer in offers])
    await session.commit()
    return
