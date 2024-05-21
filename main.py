from fastapi import FastAPI, Depends, HTTPException, status
from db_models import Base, Author, Book, Genre, SessionLocal, init_db
from routes import authors, books, book_authors, book_genre

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include routes
app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(book_authors.router, prefix="/book_author", tags=["book_author"])
app.include_router(book_genre.router, prefix="/book_genre", tags=["book_genre"])

@app.get("/")
def root():
    return {"message": "Welcome to the Book Store API!"}
