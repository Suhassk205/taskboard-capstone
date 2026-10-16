"""Serialize schema migrations across application replicas."""
import time
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from .db import engine

for attempt in range(30):
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        break
    except Exception:
        if attempt == 29:
            raise
        time.sleep(2)

with engine.connect() as connection:
    connection.execute(text("SELECT pg_advisory_lock(214210)"))
    try:
        command.upgrade(Config("alembic.ini"), "head")
    finally:
        connection.execute(text("SELECT pg_advisory_unlock(214210)"))
