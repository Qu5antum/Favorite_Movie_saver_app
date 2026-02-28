from app.database.db import Session
from app.database.models import Movie, Actor
from typing import Optional, List
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload


class MovieService:
    def __init__(self, session: Session):
        self.session = session

    def add_new_movie(
        self,
        title: str, 
        year: int, 
        description: str, 
        watched: bool = False,
        actors: Optional[List[str]] = None,
        url: str | None = None,
    ):
        new_movie = Movie(
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
                new_movie.movie_actors.append(actor)

        self.session.add(new_movie)
        self.session.commit()
        self.session.refresh(new_movie)

        return new_movie
        

    def delete_movie_by_id(self, movie_id: int):
        movie = self.session.get(Movie, movie_id)

        if not movie:
            return False

        self.session.delete(movie)
        self.session.commit()
        return True


    def get_all_movies(self, watched: bool | None = None, order: str | None = None):
            query = select(Movie).options(selectinload(Movie.movie_actors))
            
            if watched is not None:
                query = query.where(Movie.watched == watched)
            
            if order == "asc":
                query = query.order_by(Movie.year.asc())
            elif order == "desc":
                query = query.order_by(Movie.year.desc())

            result = self.session.execute(query)
            return result.scalars().all()
        
    def update_watched_movie(self, movie_id: int, watched: bool = True) -> bool:
        movie = self.session.get(Movie, movie_id)

        if not movie:
            return False

        movie.watched = watched
        self.session.commit()
        return True
        

    def search_movies(self, title: str):
        result = self.session.execute(
            select(Movie)
            .options(selectinload(Movie.movie_actors))
            .where(Movie.title.ilike(f"%{title}"))
        )
        movies = result.scalars().all()

        return movies
        

    def filter_movies_by_actor(self, actor_name: str):
        result = self.session.execute(
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
    
    def update_movie(
        self,
        movie_id: int,
        title: str | None = None,
        year: int | None = None,
        description: str | None = None,
        url: str | None = None,
        actor_list: list[str] | None = None
    ):
        movie = self.session.get(Movie, movie_id)
        if not movie:
            return False
        
        if title is not None:
            movie.title = title
        if year is not None:
            movie.year = year
        if description is not None:
            movie.description = description
        if url is not None:
            movie.url = url
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

            movie.movie_actors = actors

        self.session.commit()
        return True

    def get_movie_by_id(
        self,
        movie_id: int
    ):
        movie = self.session.get(Movie, movie_id)

        if not movie:
            return False
        
        return movie

    



        

 
    
     
        
    
