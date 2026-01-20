from app.database.db import SessionLocal
from app.database.models import Movie, Actor
from typing import Optional, List
from sqlalchemy import select, delete
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
    

def delete_movie_by_id(movie_id: int):
    with SessionLocal() as session:
        movie = session.get(Movie, movie_id)

        if not movie:
            return False

        session.delete(movie)
        session.commit()
        return True


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
    

def search_movies(title: str):
    with SessionLocal() as session:
        result = session.execute(
            select(Movie)
            .options(selectinload(Movie.actors))
            .where(Movie.title.ilike(f"%{title}"))
        )
        movies = result.scalars().all()

        return movies
    

def filter_movies_by_actor(actor_name: str):
    with SessionLocal() as session:
        result = session.execute(
            select(Movie)
            .where(
                Movie.actors.any(
                    Actor.name.ilike(f"%{actor_name}%")
                )
            )
            .options(selectinload(Movie.actors))
        )

        movies = result.scalars().all()

        return movies

    

 
    
     
        
    
