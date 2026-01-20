from app.database.db import Session
from app.database.models import Movie, Actor

session = Session()
movies = session.query(Movie).all()
actors = session.query(Actor).all()

for movie in movies:
    print(movie.title, movie.year, movie.description)


for actor in actors:
    print(actor.name)



session.close()