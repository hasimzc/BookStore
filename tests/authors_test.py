import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db_models import Base, get_db
from routes.authors import router
from routes.book_authors import router

# Configure test database
SQLALCHEMY_DATABASE_URL = "sqlite:////Users/hasimzafercicek/desktop/BookStoreTest.db"
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
    response = client.post("/authors/", json={"full_name": "Author Name", "birth_date": "1984-05-22"})
    # Debugging output to understand test failure
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.json()}")
    assert response.status_code == 200

def test_list_authors(setup_database):
    client = TestClient(app)
    response = client.get("/authors/")
    # test_create_author(setup_database)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_author_books(setup_database):
    client = TestClient(app)

    # Create a test author
    author_data = {"full_name": "Test Author", "birth_date": "1990-01-01"}
    response = client.post("/authors/", json=author_data)
    author_id = response.json()["id"]
    # Create test books and associate them with the author
    book1_data = {"title": "Test Book 1", "publication_date": "2021-01-01"}
    book2_data = {"title": "Test Book 2", "publication_date": "2022-01-01"}
    client.post("/books/", json=book1_data)
    client.post("/books/", json=book2_data)
    book1_id = client.get("/books/1").json()["id"]
    book2_id = client.get("/books/2").json()["id"]

    client.post("/book_authors/1/add_authors", json=[author_id])
    client.post("/book_authors/2/add_authors", json=[author_id])

    # Make a GET request to retrieve the author's books
    response = client.get(f"/authors/{author_id}/books")

    assert response.status_code == 200
    books = response.json()
    assert len(books) == 2
    assert books[0]["title"] == "Test Book 1"
    assert books[1]["title"] == "Test Book 2"


if __name__ == "__main__":
    pytest.main()
