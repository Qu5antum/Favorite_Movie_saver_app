from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database.base import Base
from app.database import models
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "movies.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

