from fastapi import BackgroundTasks, Body, Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import Session
from app.auth.auth import validate_token
from app.db.crud import CRUDOffer, CRUDProduct
from app.db.database import get_session
from app.models import ProductWrite, Product, ProductRead
from app.utils.utils import register_product

router = APIRouter(prefix="/products")


@router.get("/{id}", response_model=ProductRead, tags=["Product catalog"])
def get_product(id: int, session: Session = Depends(get_session)):
    return CRUDProduct.read_by_id(id=id, session=session)


@router.get("", response_model=list[ProductRead], tags=["Product catalog"])
def get_products(session: Session = Depends(get_session)):
    return CRUDProduct.read_all(session=session)


@router.post("", response_model=ProductRead, tags=["Edit products"])
async def create_product(
    product: ProductWrite,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    token: None = Depends(validate_token),
):
    if CRUDProduct.is_in_db(name=product.name, session=session):
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
    token: None = Depends(validate_token),
):
    return CRUDProduct.update_description_by_id(
        id=id, description=description, session=session
    )


@router.delete("/{id}", tags=["Edit products"])
def delete_product_by_id(
    id: int,
    session: Session = Depends(get_session),
    token: None = Depends(validate_token),
):
    CRUDProduct.delete_by_id(id=id, session=session)
    CRUDOffer.delete_all(product_id=id, session=session)
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Product {id} successfully deleted",
        },
    )
