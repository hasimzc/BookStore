from fastapi.testclient import TestClient
from main import app
from schemas import AuthorCreate, AuthorUpdate

client = TestClient(app)

def test_create_author():
    author_data = {
        "full_name": "Hasim Zafer Cicek",
        "birth_date": "2000-08-26"
    }
    response = client.post("/authors/", json=author_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Hasim Zafer Cicek"

def test_get_author():
    response = client.get("/authors/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_author():
    author_data = {
        "full_name": "Updated Author",
        "birth_date": "1990-01-01"
    }
    response = client.put("/authors/1", json=author_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Author"

def test_delete_author():
    response = client.delete("/authors/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_authors():
    response = client.get("/authors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

