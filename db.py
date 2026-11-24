import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Each teammate can set their own DATABASE_URL environment variable,
# or edit the default below for their machine (don't commit a password).
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://shreyahkarthik@localhost:5432/fitness_club",
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass