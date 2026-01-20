from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from sqlalchemy import String, Integer, Boolean, ForeignKey, Table, Column


actor_movies = Table(
    "actor_movies",
    Base.metadata,
    Column("actor_id", ForeignKey("actors.id"), primary_key=True),
    Column("movie_id", ForeignKey("movies.id"), primary_key=True)
)

actor_series = Table(
    "actor_series",
    Base.metadata,
    Column("actor_id", ForeignKey("actors.id"), primary_key=True),
    Column("series_id", ForeignKey("serieses.id"), primary_key=True)
)

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    year: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    watched: Mapped[bool] = mapped_column(Boolean, default=False)

    movie_actors: Mapped[list["Actor"]] = relationship(
        secondary=actor_movies,
        back_populates="movies"
    )


class Series(Base):
    __tablename__ = "serieses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    year: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    watched: Mapped[bool] = mapped_column(Boolean, default=False)

    series_actors: Mapped[list["Actor"]] = relationship(
        secondary=actor_series,
        back_populates="serieses"
    )



class Actor(Base):
    __tablename__ = "actors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    movies: Mapped[list["Movie"]] = relationship(
        secondary=actor_movies,
        back_populates="movie_actors"
    )

    serieses: Mapped[list["Series"]] = relationship(
        secondary=actor_movies,
        back_populates="series_actors"
    )



    




