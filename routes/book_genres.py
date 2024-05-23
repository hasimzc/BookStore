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
    def get_all_subgenre_ids(genre_id):
        # Fetch direct children first
        subgenre_ids = db.query(DBGenre.id).filter(DBGenre.parent_id == genre_id).all()
        subgenre_ids = [id for (id,) in subgenre_ids]

        all_subgenre_ids = subgenre_ids[:]
        # Recursively fetch all sub-children
        for sub_id in subgenre_ids:
            all_subgenre_ids.extend(get_all_subgenre_ids(sub_id))

        return all_subgenre_ids

    # Fetch the main genre ID
    main_genre_id = db.query(DBGenre.id).filter(DBGenre.name == genre_name).scalar()

    if not main_genre_id:
        return []

    all_genre_ids = get_all_subgenre_ids(main_genre_id)
    all_genre_ids.append(main_genre_id)

    # Query for books associated with all these genre IDs
    db_books = db.query(DBBook).join(book_genre).filter(book_genre.c.genre_id.in_(all_genre_ids)).all()

    return db_books
