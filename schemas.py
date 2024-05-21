from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class AuthorBase(BaseModel):
    full_name: str
    birth_date: date

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List['Book'] = []

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    publication_date: date

class BookCreate(BookBase):
    author_ids: List[int]
    genre_ids: List[int]

class Book(BookBase):
    id: int
    authors: List[Author] = []
    genres: List['Genre'] = []

    class Config:
        orm_mode = True

class GenreBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class Genre(GenreBase):
    id: int
    subgenres: List['Genre'] = []

    class Config:
        orm_mode = True
