import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db_models import Base, get_db
from routes.book_authors import router

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
app.include_router(router, prefix="/book")


# Create the test database
@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)



# Util function to create authors and book for tests
def create_author(client, full_name, birth_date):
    response = client.post("/author/", json={"full_name": full_name, "birth_date": birth_date})
    return response.json()


def create_book(client, title, publication_date):
    response = client.post("/books/", json={"title": title, "publication_date": publication_date})
    return response.json()


def test_add_authors_to_book(setup_database):
    client = TestClient(app)

    # Creating authors
    author1 = create_author(client, "Author One", "1980-01-01")
    author2 = create_author(client, "Author Two", "1985-01-01")

    # Creating a book
    book = create_book(client, "Test Book", "2024-01-01")

    # Adding authors to the book
    response = client.post(f"/book/{book['id']}/add_authors", json=[author1['id'], author2['id']])

    assert response.status_code == 200


def test_add_author_to_nonexistent_book(setup_database):
    client = TestClient(app)

    # Creating an author
    author = create_author(client, "Author Three", "1990-01-01")

    # Trying to add this author to a non-existent book
    response = client.post("/book/9999/add_authors", json=[author['id']])

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_add_nonexistent_author_to_book(setup_database):
    client = TestClient(app)

    # Creating a book
    book = create_book(client, "Another Test Book", "2024-01-01")

    # Trying to add a non-existent author to this book
    response = client.post(f"/book/{book['id']}/add_authors", json=[9999])

    assert response.status_code == 404
    assert response.json()["detail"] == "Author with id 9999 not found"


if __name__ == "__main__":
    pytest.main()
