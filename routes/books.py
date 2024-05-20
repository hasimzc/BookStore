from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import BookCreate, BookUpdate, Book
from crud import create_book, get_book, update_book, delete_book
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Book)
def create_new_book(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db=db, book=book)

@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=Book)
def update_book_details(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    updated_book = update_book(db, book_id=book_id, book=book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{book_id}", response_model=Book)
def delete_book_by_id(book_id: int, db: Session = Depends(get_db)):
    deleted_book = delete_book(db, book_id=book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book
