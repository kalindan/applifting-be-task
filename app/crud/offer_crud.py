from sqlmodel import Session, select

from app.models import Offer


def create(offer: Offer, session: Session) -> Offer:
    session.add(offer)
    session.commit()
    session.refresh(offer)
    return offer


def read_by_id(id: int, session: Session) -> Offer | None:
    offer = session.get(Offer, id)
    if not offer:
        return None
    return offer


def update(offer: Offer, session: Session) -> Offer:
    session.add(offer)
    session.commit()
    session.refresh(offer)
    return offer


def delete_all(product_id, session: Session):
    offers = session.exec(
        select(Offer).where(Offer.product_id == product_id)
    ).all()
    for offer in offers:
        session.delete(offer)
    session.commit()
    return
