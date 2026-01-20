from app.database.db import SessionLocal
from app.database.models import Series, Actor
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload


def add_series(
    title: str,
    year: int,
    description: str | None = None,
    watched: bool = False,
    actors: Optional[List[str]] = None
):
    with SessionLocal() as session:
        new_series = Series(
            title=title,
            year=year,
            description=description,
            watched=watched,
        )

        if actors:
            existing = session.execute(
                select(Actor).where(Actor.name.in_([a.strip() for a in actors]))
            ).scalars().all()
            actor_map = {a.name: a for a in existing}

            for name in actors:
                name = name.strip()
                actor = actor_map.get(name)
                if not actor:
                    actor = Actor(name=name)
                    session.add(actor)
                    session.flush()
                new_series.series_actors.append(actor)

        session.add(new_series)
        session.commit()
        session.refresh(new_series)

        return new_series


def delete_series_by_id(movie_id: int):
    with SessionLocal() as session:
        movie = session.get(Series, movie_id)

        if not movie:
            return False

        session.delete(movie)
        session.commit()
        return True
    
def get_all_serieses():
    with SessionLocal() as session:
        movies = session.execute(
            select(Series)
            .options(selectinload(Series.series_actors))
        )
        
        return movies.scalars().all()
    

def update_watched_series(series_id: int, watched: bool = True) -> bool:
    with SessionLocal() as session:
        series = session.get(Series, series_id)

        if not series:
            return False

        series.watched = watched
        session.commit()
        return True
    


def search_serises(title: str):
    with SessionLocal() as session:
        result = session.execute(
            select(Series)
            .options(selectinload(Series.series_actors))
            .where(Series.title.ilike(f"%{title}"))
        )
        serieses = result.scalars().all()

        return serieses
    

def filter_serieses_by_actor(actor_name: str):
    with SessionLocal() as session:
        result = session.execute(
            select(Series)
            .where(
                Series.movie_actors.any(
                    Actor.name.ilike(f"%{actor_name}%")
                )
            )
            .options(selectinload(Series.movie_actors))
        )

        serieses = result.scalars().all()

        return serieses
    