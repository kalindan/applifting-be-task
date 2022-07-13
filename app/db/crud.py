from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Product
from app.models.offer_model import Offer


class CRUDProduct:
    @staticmethod
    def create(product: Product, session: Session) -> Product:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

    @staticmethod
    def read_by_name(name: str, session: Session) -> Product:
        product = session.exec(
            select(Product).where(Product.name == name)
        ).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    def read_by_id(id: int, session: Session) -> Product:
        product = session.get(Product, id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    def read_all(session: Session) -> list[Product]:
        return session.exec(select(Product)).all()

    @staticmethod
    def delete_by_name(name: str, session: Session) -> None:
        product = session.exec(
            select(Product).where(Product.name == name)
        ).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        session.delete(product)
        session.commit()
        return

    @staticmethod
    def delete_by_id(id: int, session: Session) -> None:
        product = session.get(Product, id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        session.delete(product)
        session.commit()
        return

    @staticmethod
    def is_in_db(name: str, session: Session) -> bool:
        product = session.exec(
            select(Product).where(Product.name == name)
        ).first()
        if not product:
            return False
        return True


class CRUDOffer:
    @staticmethod
    def create(offer: Offer, session: Session) -> Offer:
        session.add(offer)
        session.commit()
        session.refresh(offer)
        return offer

    @staticmethod
    def delete_all(product_id, session: Session):
        offers = session.exec(
            select(Offer).where(Offer.product_id == product_id)
        ).all()
        for offer in offers:
            session.delete(offer)
        session.commit()
        return
