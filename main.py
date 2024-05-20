from fastapi import FastAPI
from routes import authors , books #, genres
from database import Base, engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(books.router, prefix="/books", tags=["books"])
# app.include_router(genres.router, prefix="/genres", tags=["genres"])

@app.get("/")
def root():
    return {"message": "Welcome to the Book Store API!"}
