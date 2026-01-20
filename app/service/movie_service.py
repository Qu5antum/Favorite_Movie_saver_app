from app.database.db import SessionLocal
from app.database.models import Movie, Actor
from typing import Optional, List
from sqlalchemy import select 
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError


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

        for name in actors:
                name = name.strip()

                try:
                    actor = Actor(name=name)
                    session.add(actor)
                    session.flush()   # проверка unique

                except IntegrityError:
                    session.rollback()
                    actor = session.execute(
                        select(Actor).where(Actor.name == name)
                    ).scalar_one()

                new_movie.actors.append(actor)

        session.add(new_movie)
        session.commit()
        session.refresh(new_movie)

        return new_movie
    


def get_all_movies():
    with SessionLocal() as session:
        movies = session.execute(
            select(Movie)
            .options(selectinload(Movie.actors))
        )
        
        return movies.scalars().all()
    
def update_watched(movie_id: int, watched: bool = True) -> bool:
    with SessionLocal() as session:
        movie = session.get(Movie, movie_id)

        if not movie:
            return False

        movie.watched = watched
        session.commit()
        return True

 
    
     
        
    
