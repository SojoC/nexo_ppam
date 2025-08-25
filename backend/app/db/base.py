from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://nexo:nexo@localhost:5432/nexo")

class Base(DeclarativeBase):
    pass

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
