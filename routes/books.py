from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db_models import Book as DBBook, Author, Genre, book_author, book_genre, get_db
from schemas import Book, BookCreate
from typing import List

router = APIRouter()

@router.post("/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    publication_date = datetime.strptime(book.publication_date, "%Y-%m-%d").date()
    db_book = DBBook(title=book.title, publication_date=publication_date)

    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Fetch authors
    authors = db.query(Author).join(book_author).filter(book_author.c.book_id == book_id).all()
    author_details = [{"id": author.id, "full_name": author.full_name, "birth_date": author.birth_date} for author in
                      authors]

    # Fetch genres
    genres = db.query(Genre).join(book_genre).filter(book_genre.c.book_id == book_id).all()
    genre_details = [{"id": genre.id, "name": genre.name, "parent_id": genre.parent_id} for genre in genres]

    return {
        "id": db_book.id,
        "title": db_book.title,
        "publication_date": db_book.publication_date,
        "authors": author_details,
        "genres": genre_details,
    }


@router.get("/", response_model=List[Book])
def list_books(db: Session = Depends(get_db)):
    try:
        return db.query(DBBook).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occured while retrieving authors")

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        if key == "publication_date":
            value = datetime.strptime(value, "%Y-%m-%d").date()
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book
