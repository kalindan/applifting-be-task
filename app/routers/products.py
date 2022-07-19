from fastapi import BackgroundTasks, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth import jwt_bearer
from app.crud import offer_crud, product_crud
from app.db import get_session
from app.models import Product, ProductRead, ProductReadWithOffers, ProductWrite
from app.utils import get_offers_by_product_id, register_product

router = APIRouter(prefix="/products")


@router.get(
    "/{id}", response_model=ProductReadWithOffers, tags=["Product catalog"]
)
async def get_product_with_offers(
    id: int, session: AsyncSession = Depends(get_session)
):
    product = await product_crud.read_by_id(id=id, session=session)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("", response_model=list[ProductRead], tags=["Product catalog"])
async def get_products(session: AsyncSession = Depends(get_session)):
    products = await product_crud.read_all(session=session)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products


@router.post("", response_model=ProductRead, tags=["Edit products"])
async def create_product(
    product: ProductWrite,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    jwt: None = Depends(jwt_bearer),
):
    is_in_catalog = await product_crud.read_by_name(
        name=product.name, session=session
    )
    if is_in_catalog:
        raise HTTPException(status_code=406, detail="Product already exists")
    product_db = await product_crud.create(
        product=Product.from_orm(product), session=session
    )
    background_tasks.add_task(register_product, product_db)
    background_tasks.add_task(get_offers_by_product_id, product_db.id)
    return product_db


@router.patch("/{id}", response_model=ProductRead, tags=["Edit products"])
async def update_product_description(
    id: int,
    description: str = Body(embed=True),
    session: AsyncSession = Depends(get_session),
    jwt: None = Depends(jwt_bearer),
):
    product = await product_crud.read_by_id(id=id, session=session)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.description = description
    product_in_db = await product_crud.update(product=product, session=session)
    return product_in_db


@router.delete("/{id}", tags=["Edit products"])
async def delete_product(
    id: int,
    session: AsyncSession = Depends(get_session),
    jwt: None = Depends(jwt_bearer),
):
    product = await product_crud.read_by_id(id=id, session=session)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await product_crud.delete(product=product, session=session)
    await offer_crud.delete_all_by_product_id(product_id=id, session=session)
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Product {id} successfully deleted",
        },
    )
