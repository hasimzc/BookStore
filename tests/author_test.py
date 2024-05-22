import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db_models import Base, get_db
from routes.author import router

# Configure test database
SQLALCHEMY_DATABASE_URL = "sqlite:////Users/hasimzafercicek/desktop/bookstore.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency with a testing session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        pass

# Apply overrides and include router
app.dependency_overrides[get_db] = override_get_db
app.include_router(router, prefix="/author")

# Create the test database
@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_author(setup_database):
    client = TestClient(app)
    response = client.post("/author/", json={"full_name": "Author Name", "birth_date": "1984-05-22"})
    # Debugging output to understand test failure
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.json()}")
    assert response.status_code == 200

def test_list_authors(setup_database):
    client = TestClient(app)
    response = client.get("/author/")
    # test_create_author(setup_database)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

if __name__ == "__main__":
    pytest.main()
