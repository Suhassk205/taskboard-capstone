import os
os.environ["DATABASE_URL"]="sqlite://"
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.db import Base,get_db
from app.main import app

@pytest.fixture
def client():
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    def test_db():
        with Session() as db:yield db
    app.dependency_overrides[get_db]=test_db
    with TestClient(app) as c:yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine);engine.dispose()
