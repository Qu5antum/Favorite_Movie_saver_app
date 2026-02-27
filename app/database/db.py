from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from pathlib import Path
import sys

from app.database import models
from .base import Base


def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_dir()
DB_PATH = BASE_DIR / "movies.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False}
)

Base.metadata.create_all(bind=engine)

def get_db():
    with Session(engine, autoflush=False, autocommit=False) as session:
        yield session
