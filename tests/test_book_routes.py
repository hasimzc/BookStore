from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_book():
    book_data = {
        "title": "Test Book",
        "publication_date": "2023-01-01"
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

def test_read_book():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_book():
    book_data = {
        "title": "Updated Test Book"
    }
    response = client.put("/books/1", json=book_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Book"

def test_delete_book():
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_read_nonexistent_book():
    response = client.get("/books/999")
    assert response.status_code == 404

def test_update_nonexistent_book():
    book_data = {
        "title": "Updated Nonexistent Book"
    }
    response = client.put("/books/999", json=book_data)
    assert response.status_code == 404

def test_delete_nonexistent_book():
    response = client.delete("/books/999")
    assert response.status_code == 404
