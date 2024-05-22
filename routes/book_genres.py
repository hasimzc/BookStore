from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_models import Book as DBBook, Genre as DBGenre, book_genre, get_db
from schemas import Book, Genre
from typing import List

router = APIRouter()

@router.post("/{book_id}/add_genres", response_model=Book)
def add_genres_to_book(book_id: int, genre_ids: List[int], db: Session = Depends(get_db)):
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    for genre_id in genre_ids:
        db_genre = db.query(DBGenre).filter(DBGenre.id == genre_id).first()
        if db_genre is None:
            raise HTTPException(status_code=404, detail=f"Genre with id {genre_id} not found")

        # Create a new entry in the book_genre table
        db_book_genre = book_genre.insert().values(book_id=book_id, genre_id=genre_id)
        db.execute(db_book_genre)

    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/genre/{genre_name}/books", response_model=List[Book])
def list_books_by_genre(genre_name: str, db: Session = Depends(get_db)):
    genre_subquery = db.query(DBGenre.id).filter(DBGenre.name == genre_name).subquery()

    db_books = db.query(DBBook).join(book_genre).join(DBGenre).filter(
        (DBGenre.id == genre_subquery) | (DBGenre.parent_id == genre_subquery)
    ).all()

    return db_books
