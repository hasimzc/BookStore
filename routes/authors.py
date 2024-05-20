from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from schemas import AuthorCreate, AuthorUpdate, Author
from crud import create_author, get_author, update_author, delete_author , get_authors

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Author)
def create_author_endpoint(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(db=db, author=author)

@router.get("/{author_id}", response_model=Author)
def get_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    db_author = get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@router.put("/{author_id}", response_model=Author)
def update_author_endpoint(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    db_author = update_author(db=db, author_id=author_id, author=author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@router.delete("/{author_id}", response_model=Author)
def delete_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    db_author = delete_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@router.get("/", response_model=List[Author])
def get_authors_endpoint(db: Session = Depends(get_db)):
    authors = get_authors(db=db)
    return authors

