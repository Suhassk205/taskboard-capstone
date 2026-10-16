import os
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

url = os.getenv("DATABASE_URL") or URL.create("postgresql+psycopg", username="campusdesk", password=os.getenv("DATABASE_PASSWORD", ""), host=os.getenv("DATABASE_HOST", "postgres"), database="campusdesk")
engine = create_engine(url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as session:
        yield session
