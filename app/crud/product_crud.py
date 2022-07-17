from sqlmodel import Session, select

from app.models import Product


def create(product: Product, session: Session) -> Product:
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def read_by_name(name: str, session: Session) -> Product | None:
    product = session.exec(select(Product).where(Product.name == name)).first()
    if not product:
        return None
    return product


def read_by_id(id: int, session: Session) -> Product | None:
    product = session.get(Product, id)
    if not product:
        return None
    return product


def read_all(session: Session) -> list[Product]:
    return session.exec(select(Product)).all()


def update(product: Product, session: Session) -> Product:
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def delete(product: Product, session: Session) -> None:
    session.delete(product)
    session.commit()
    return
