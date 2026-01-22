from app.database.db import SessionLocal
from app.database.models import Movie, Actor
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload


def add_new_movie(
    title: str, 
    year: int, 
    description: str, 
    watched: bool = False,
    actors: Optional[List[str]] = None
):
    with SessionLocal() as session:
        new_movie = Movie(
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
                new_movie.movie_actors.append(actor)

        session.add(new_movie)
        session.commit()
        session.refresh(new_movie)

        return new_movie
    

def delete_movie_by_id(movie_id: int):
    with SessionLocal() as session:
        movie = session.get(Movie, movie_id)

        if not movie:
            return False

        session.delete(movie)
        session.commit()
        return True


def get_all_movies(order: str | None = None):
    with SessionLocal() as session:
        query = select(Movie).options(selectinload(Movie.movie_actors))

        if order == "asc":
            query = query.order_by(Movie.year.asc())
        elif order == "desc":
            query = query.order_by(Movie.year.desc())

        result = session.execute(query)
        return result.scalars().all()
    
def update_watched_movie(movie_id: int, watched: bool = True) -> bool:
    with SessionLocal() as session:
        movie = session.get(Movie, movie_id)

        if not movie:
            return False

        movie.watched = watched
        session.commit()
        return True
    

def search_movies(title: str):
    with SessionLocal() as session:
        result = session.execute(
            select(Movie)
            .options(selectinload(Movie.movie_actors))
            .where(Movie.title.ilike(f"%{title}"))
        )
        movies = result.scalars().all()

        return movies
    

def filter_movies_by_actor(actor_name: str):
    with SessionLocal() as session:
        result = session.execute(
            select(Movie)
            .where(
                Movie.movie_actors.any(
                    Actor.name.ilike(f"%{actor_name}%")
                )
            )
            .options(selectinload(Movie.movie_actors))
        )

        movies = result.scalars().all()

        return movies

    

 
    
     
        
    
