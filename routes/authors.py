from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db_models import Author as DBAuthor, get_db, Book as DBBook, book_author
from schemas import Author, AuthorCreate, Book
from typing import List

router = APIRouter()

@router.post("/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = DBAuthor(full_name=author.full_name, birth_date=author.birth_date)
    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@router.get("/", response_model=List[Author])
def list_authors(db: Session = Depends(get_db)):
    try:
        return db.query(DBAuthor).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured while retrieving authors")

@router.get("/{author_id}/books", response_model=List[Book])
def get_author_books(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(DBAuthor).filter(DBAuthor.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    db_books = db.query(DBBook).join(DBBook.authors).filter(DBAuthor.id == author_id).all()
    return db_books

