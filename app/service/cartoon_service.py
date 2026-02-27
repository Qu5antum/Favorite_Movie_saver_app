from app.database.db import Session
from app.database.models import Cartoon
from sqlalchemy import select


class CartoonService:
    def __init__(self, session: Session):
        self.session = session

    def add_cartoon(
        self,
        title: str,
        year: int,
        cartoon_type: str,
        description: str | None = None,
        watched: bool = False,
    ):
        new_cartoon = Cartoon(
            title=title,
            year=year,
            cartoon_type=cartoon_type,
            description=description,
            watched=watched
        )

        self.session.add(new_cartoon)
        self.session.commit()
        self.session.refresh(new_cartoon)

        return new_cartoon
        

    def delete_cartoon_by_id(self, cartoon_id: int):
        cartoon = self.session.get(Cartoon, cartoon_id)

        if not cartoon:
            return False

        self.session.delete(cartoon)
        self.session.commit()
        return True
    

    def get_all_cartoons(self, watched: bool | None = None, order: str | None = None):
        query = select(Cartoon)

        if watched is not None:
            query = query.where(Cartoon.watched == watched)

        if order == "asc":
            query = query.order_by(Cartoon.year.asc())
        elif order == "desc":
            query = query.order_by(Cartoon.year.desc())

        result = self.session.execute(query)
        return result.scalars().all()
        

    def search_cartoon_by_title(self, title: str):
        result = self.session.execute(
            select(Cartoon)
            .where(Cartoon.title.ilike(f"%{title}"))
        )
        cartoons = result.scalars().all()

        return cartoons
    
        
    def update_watched_cartoon(self, cartoo_id: int, watched: bool = True) -> bool:
        cartoon = self.session.get(Cartoon, cartoo_id)

        if not cartoon:
            return False

        cartoon.watched = watched
        self.session.commit()
        return True






