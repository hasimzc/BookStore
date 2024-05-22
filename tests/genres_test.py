import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db_models import Base, get_db, Genre as DBGenre, Book as DBBook
from routes.genres import router
from datetime import date

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
app.include_router(router, prefix="/genres")

# Create the test database
@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Fixture to populate test data
@pytest.fixture(scope="module")
def populate_test_data(setup_database):
    db = TestingSessionLocal()
    genre1 = DBGenre(name="Genre 1")
    genre2 = DBGenre(name="Genre 2")
    book1 = DBBook(title="Book 1", publication_date=date(2021, 1, 1))
    book2 = DBBook(title="Book 2", publication_date=date(2021, 2, 1))
    genre1.books.extend([book1, book2])
    db.add_all([genre1, genre2, book1, book2])
    db.commit()
    db.close()

def test_list_genres_with_books(populate_test_data):
    client = TestClient(app)
    response = client.get("/genres/")
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main()
