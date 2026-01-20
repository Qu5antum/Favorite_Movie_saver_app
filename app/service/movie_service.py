from app.database.db import Session
from app.database.models import Movie, Actor
from typing import Optional, List


def add_new_movie(
    title: str, 
    year: int, 
    description: str, 
    watched: bool = False,
    actors: Optional[List[str]] = None
):
    session = Session()
    
    try:
        new_movie = Movie(
            title=title,
            year=year,
            description=description,
            watched=watched,
        )

        if actors:
            for actor_name in actors:
                actor = (
                    session.query(Actor)
                    .filter(Actor.name == actor_name)
                    .first()
                )

                if not actor:
                    actor = Actor(name=actor_name)

                new_movie.actors.append(actor)

        session.add(new_movie)
        session.commit()
        session.refresh(new_movie)

        return new_movie
    
    finally:
        session.close()
    
