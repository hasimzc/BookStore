import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db_models import Base, get_db
from routes.books import router

# Configure test database
SQLALCHEMY_DATABASE_URL = "sqlite:////Users/hasimzafercicek/desktop/test_bookstore.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency with a testing session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply overrides and include router
app.dependency_overrides[get_db] = override_get_db
app.include_router(router, prefix="/books")

# Create the test database
@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_book(setup_database):
    client = TestClient(app)
    response = client.post("/books/", json={"title": "Book Title", "publication_date": "2023-06-07"})
    assert response.status_code == 200
    assert response.json()["title"] == "Book Title"

def test_get_book(setup_database):
    client = TestClient(app)
    book = client.post("/books/", json={"title": "Book Title", "publication_date": "2023-06-07"}).json()
    response = client.get(f"/books/{book['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Book Title"

def test_list_books(setup_database):
    client = TestClient(app)
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_book(setup_database):
    client = TestClient(app)
    book = client.post("/books/", json={"title": "Book Title", "publication_date": "2023-06-07"}).json()
    response = client.delete(f"/books/{book['id']}")
    assert response.status_code == 204
    assert client.get(f"/books/{book['id']}").status_code == 404

def test_update_book(setup_database):
    client = TestClient(app)
    book = client.post("/books/", json={"title": "Book Title", "publication_date": "2023-06-07"}).json()
    response = client.put(f"/books/{book['id']}", json={"title": "Updated Book Title", "publication_date": "2023-06-08"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Book Title"

if __name__ == "__main__":
    pytest.main()
