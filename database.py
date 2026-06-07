from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.course import Course
from app.models.user import User
from app.models import Base


DATABASE_URL = "sqlite:///courses.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
