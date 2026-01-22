from app.database.db import SessionLocal
from app.database.models import Cartoon
from sqlalchemy import select
from sqlalchemy.orm import selectinload


def add_cartoon(
    title: str,
    year: int,
    cartoon_type: str,
    description: str | None = None,
    watched: bool = False,
):
    with SessionLocal() as session: 
        new_cartoon = Cartoon(
            title=title,
            year=year,
            cartoon_type=cartoon_type,
            description=description,
            watched=watched
        )

        session.add(new_cartoon)
        session.commit()
        session.refresh(new_cartoon)

        return new_cartoon
    

def delete_cartoon_by_id(cartoon_id: int):
     with SessionLocal() as session:
        cartoon = session.get(Cartoon, cartoon_id)

        if not cartoon:
            return False

        session.delete(cartoon)
        session.commit()
        return True
     

def get_all_cartoons(order: str | None = None):
    with SessionLocal() as session:
        query = select(Cartoon)

        if order == "asc":
            query = query.order_by(Cartoon.year.asc())
        elif order == "desc":
            query = query.order_by(Cartoon.year.desc())

        result = session.execute(query)
        return result.scalars().all()
    

def search_cartoon_by_title(title: str):
    with SessionLocal() as session:
        result = session.execute(
            select(Cartoon)
            .where(Cartoon.title.ilike(f"%{title}"))
        )
        cartoons = result.scalars().all()

        return cartoons
    
    
def update_watched_cartoon(cartoo_id: int, watched: bool = True) -> bool:
    with SessionLocal() as session:
        cartoon = session.get(Cartoon, cartoo_id)

        if not cartoon:
            return False

        cartoon.watched = watched
        session.commit()
        return True






