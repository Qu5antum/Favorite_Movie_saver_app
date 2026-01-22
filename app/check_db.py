from app.database.db import SessionLocal
from app.database.models import Movie, Actor, Series

session = SessionLocal()
movies = session.query(Movie).all()
actors = session.query(Actor).all()
serieses = session.query(Series).all()



for actor in actors:
    print(actor.name)



session.close()