from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.database.models import Actor

def get_or_create_actor(session, name: str) -> Actor:
    