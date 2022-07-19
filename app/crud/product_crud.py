from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Product


async def create(product: Product, session: AsyncSession) -> Product:
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def read_by_name(name: str, session: AsyncSession) -> Product | None:
    result = await session.execute(select(Product).where(Product.name == name))
    product = result.scalars().first()
    if not product:
        return None
    return product


async def read_by_id(id: int, session: AsyncSession) -> Product | None:
    result = await session.execute(
        select(Product)
        .where(Product.id == id)
        .options(selectinload(Product.offers))
    )
    product = result.scalars().first()
    if not product:
        return None
    return product


async def read_all(session: AsyncSession) -> list[Product] | None:
    result = await session.execute(select(Product))
    if not result:
        return None
    return result.scalars().all()


async def update(product: Product, session: AsyncSession) -> Product:
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def delete(product: Product, session: AsyncSession) -> None:
    await session.delete(product)
    await session.commit()
    return
