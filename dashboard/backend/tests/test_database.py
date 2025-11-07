import pytest
from sqlalchemy import inspect
from app.database import engine, Base

def test_services_table_exists():
    inspector = inspect(engine)
    assert "services" in inspector.get_table_names()
