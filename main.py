from fastapi import FastAPI, Depends, HTTPException, status
from db_models import Base, Author, Book, Genre, SessionLocal, init_db
from routes import authors, books, book_authors ,book_genres, genres

app = FastAPI()

# Include routes
app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(book_authors.router, prefix="/book_authors", tags=["book_authors"])
app.include_router(book_genres.router, prefix="/book_genres", tags=["book_genres"])
app.include_router(genres.router, prefix="/genres", tags=["genres"])

@app.get("/")
def root():
    return {"message": "Welcome to the Book Store API!"}

@app.on_event("startup")
def on_startup():
    init_db()
