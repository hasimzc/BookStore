from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert
from sqlalchemy.orm import Session
from db_models import Book as DBBook, Author as DBAuthor, book_author, get_db
from schemas import Book
from typing import List

router = APIRouter()


@router.post("/{book_id}/add_authors", response_model=Book)
def add_authors_to_book(book_id: int, author_ids: List[int], db: Session = Depends(get_db)):
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    for author_id in author_ids:
        db_author = db.query(DBAuthor).filter(DBAuthor.id == author_id).first()
        if db_author is None:
            raise HTTPException(status_code=404, detail=f"Author with id {author_id} not found")

        # Insert into book_author table
        db.execute(insert(book_author).values(book_id=book_id, author_id=author_id))

    db.commit()
    db.refresh(db_book)
    return db_book
