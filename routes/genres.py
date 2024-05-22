from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db_models import Genre as DBGenre, get_db
from schemas import GenreResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[GenreResponse])
def list_genres_with_books(db: Session = Depends(get_db)):
    genres = db.query(DBGenre).filter(DBGenre.books.any()).all()
    return genres


