import pytest
from app.database import Base, engine

@pytest.fixture(autouse=True)
def setup_db():
    # Wipe and recreate database tables before every test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield