from sqlalchemy.orm import Session
from db_models import Author, Book
from schemas import AuthorCreate, AuthorUpdate, BookCreate, BookUpdate

# Author CRUD operations

def create_author(db: Session, author: AuthorCreate):
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_author(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()

def update_author(db: Session, author_id: int, author: AuthorUpdate):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author:
        for field, value in author.dict(exclude_unset=True).items():
            setattr(db_author, field, value)
        db.commit()
        db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: int):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author

def get_authors(db: Session):
    return db.query(Author).all()

# Book CRUD operations

def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book(db: Session, book_id: int, book: BookUpdate):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        for field, value in book.dict(exclude_unset=True).items():
            setattr(db_book, field, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book