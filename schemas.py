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

class GenreBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class Genre(GenreBase):
    id: int
    subgenres: List['Genre'] = []

    class Config:
        orm_mode = True

class AuthorResponse(BaseModel):
    id: int
    full_name: str
    birth_date: Optional[str] = None

class GenreResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None

class Book(BaseModel):
    id: int
    title: str
    publication_date: Optional[date]

    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str
    publication_date: Optional[str]