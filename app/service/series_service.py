from app.database.db import Session
from app.database.models import Series, Actor
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class SeriesService:
    def __init__(self, session: Session):
        self.session = session

    def add_series(
        self, 
        title: str,
        year: int,
        description: str | None = None,
        watched: bool = False,
        actors: Optional[List[str]] = None,
        url: str | None = None,
    ):
        new_series = Series(
            title=title,
            year=year,
            description=description,
            watched=watched,
            url = url
        )

        if actors:
            existing = self.session.execute(
                select(Actor).where(Actor.name.in_([a.strip() for a in actors]))
            ).scalars().all()
            actor_map = {a.name: a for a in existing}

            for name in actors:
                name = name.strip().title()
                actor = actor_map.get(name)
                if not actor:
                    actor = Actor(name=name)
                    self.session.add(actor)
                    self.session.flush()
                new_series.series_actors.append(actor)

        self.session.add(new_series)
        self.session.commit()
        self.session.refresh(new_series)

        return new_series


    def delete_series_by_id(self, movie_id: int):
        movie = self.session.get(Series, movie_id)

        if not movie:
            return False

        self.session.delete(movie)
        self.session.commit()
        return True
        
    def get_all_serieses(self, watched: bool | None = None, order: str | None = None):
        query = select(Series).options(selectinload(Series.series_actors))

        if watched is not None:
            query = query.where(Series.watched == watched)

        if order == "asc":
            query = query.order_by(Series.year.asc())
        elif order == "desc":
            query = query.order_by(Series.year.desc())

        result = self.session.execute(query)
        return result.scalars().all()
        

    def update_watched_series(self, series_id: int, watched: bool = True) -> bool:
        series = self.session.get(Series, series_id)

        if not series:
            return False

        series.watched = watched
        self.session.commit()
        return True
        


    def search_serises(self, title: str):
        result = self.session.execute(
            select(Series)
            .options(selectinload(Series.series_actors))
            .where(Series.title.ilike(f"%{title}"))
        )
        serieses = result.scalars().all()

        return serieses
    

    def filter_serieses_by_actor(self, actor_name: str):
        result = self.session.execute(
            select(Series)
            .where(
                Series.series_actors.any(
                    Actor.name.ilike(f"%{actor_name}%")
                )
            )
            .options(selectinload(Series.series_actors))
        )

        serieses = result.scalars().all()

        return serieses
    
    def update_series(
        self,
        series_id: int,
        title: str | None = None,
        year: int | None = None,
        description: str | None = None,
        url: str | None = None,
        actor_list: list[str] | None = None,
    ):
        series = self.session.get(Series, series_id)
        if not series:
            return False
        
        if title is not None:
            series.title = title
        if year is not None:
            series.year = year
        if description is not None:
            series.description = description
        if url is not None:
            series.url = url
        if actor_list is not None:
            actors = []
            for name in actor_list:
                name = name.strip().title()

                if not name:
                    continue

                actor = self.session.query(Actor).filter_by(name=name).first()

                if not actor:
                    actor = Actor(name=name)
                    self.session.add(actor)
                    self.session.flush()
                
                actors.append(actor)

            series.movie_actors = actors

        self.session.commit()
        return True
        