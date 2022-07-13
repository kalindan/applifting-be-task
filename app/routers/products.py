from fastapi import BackgroundTasks, Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import Session
from app.db.crud import CRUDOffer, CRUDProduct
from app.db.database import get_session
from app.models import ProductWrite, Product, ProductRead
from app.utils.utils import register_product

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductRead)
async def create_product(
    product: ProductWrite,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    if CRUDProduct.is_in_db(name=product.name, session=session):
        raise HTTPException(status_code=406, detail="Product already exists")
    product_db = CRUDProduct.create(
        product=Product.from_orm(product), session=session
    )
    background_tasks.add_task(register_product, product_db)
    return product_db


@router.get("/{id}", response_model=ProductRead)
def get_product(id: int, session: Session = Depends(get_session)):
    return CRUDProduct.read_by_id(id=id, session=session)


@router.get("", response_model=list[ProductRead])
def get_products(session: Session = Depends(get_session)):
    return CRUDProduct.read_all(session=session)


@router.delete("/{id}")
def delete_product_by_id(id: int, session: Session = Depends(get_session)):
    CRUDProduct.delete_by_id(id=id, session=session)
    CRUDOffer.delete_all(product_id=id, session=session)
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Product {id} successfully deleted",
        },
    )
