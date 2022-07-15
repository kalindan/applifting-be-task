from fastapi import BackgroundTasks, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlmodel import Session

from app.auth import jwt_bearer
from app.db import CRUDOffer, CRUDProduct, get_session
from app.models import Product, ProductRead, ProductReadWithOffers, ProductWrite
from app.utils import register_product

router = APIRouter(prefix="/products")


@router.get(
    "/{id}", response_model=ProductReadWithOffers, tags=["Product catalog"]
)
def get_product_with_offers(id: int, session: Session = Depends(get_session)):
    product = CRUDProduct.read_by_id(id=id, session=session)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("", response_model=list[ProductRead], tags=["Product catalog"])
def get_products(session: Session = Depends(get_session)):
    return CRUDProduct.read_all(session=session)


@router.post("", response_model=ProductRead, tags=["Edit products"])
async def create_product(
    product: ProductWrite,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    jwt: None = Depends(jwt_bearer),
):
    if CRUDProduct.read_by_name(name=product.name, session=session):
        raise HTTPException(status_code=406, detail="Product already exists")
    product_db = CRUDProduct.create(
        product=Product.from_orm(product), session=session
    )
    background_tasks.add_task(register_product, product_db)
    return product_db


@router.patch("/{id}", response_model=ProductRead, tags=["Edit products"])
def update_product_description(
    id: int,
    description: str = Body(embed=True),
    session: Session = Depends(get_session),
    jwt: None = Depends(jwt_bearer),
):
    product = CRUDProduct.read_by_id(id=id, session=session)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.description = description
    return CRUDProduct.update(product=product, session=session)


@router.delete("/{id}", tags=["Edit products"])
def delete_product(
    id: int,
    session: Session = Depends(get_session),
    jwt: None = Depends(jwt_bearer),
):
    product = CRUDProduct.read_by_id(id=id, session=session)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    CRUDProduct.delete(product=product, session=session)
    CRUDOffer.delete_all(product_id=id, session=session)
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Product {id} successfully deleted",
        },
    )
