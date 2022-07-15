from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Offer, Product


class CRUDProduct:
    @staticmethod
    def create(product: Product, session: Session) -> Product:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

    @staticmethod
    def read_by_name(name: str, session: Session) -> Product | None:
        product = session.exec(
            select(Product).where(Product.name == name)
        ).first()
        if not product:
            return None
        return product

    @staticmethod
    def read_by_id(id: int, session: Session) -> Product | None:
        product = session.get(Product, id)
        if not product:
            return None
        return product

    @staticmethod
    def read_all(session: Session) -> list[Product]:
        return session.exec(select(Product)).all()

    @staticmethod
    def update(product: Product, session: Session) -> Product:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

    @staticmethod
    def delete(product: Product, session: Session) -> None:
        session.delete(product)
        session.commit()
        return


class CRUDOffer:
    @staticmethod
    def create(offer: Offer, session: Session) -> Offer:
        session.add(offer)
        session.commit()
        session.refresh(offer)
        return offer

    @staticmethod
    def read_by_id(id: int, session: Session) -> Offer | None:
        offer = session.get(Offer, id)
        if not offer:
            return None
        return offer

    @staticmethod
    def update(offer: Offer, session: Session) -> Offer:
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
