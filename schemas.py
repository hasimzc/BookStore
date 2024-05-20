from pydantic import BaseModel
from datetime import date

class AuthorBase(BaseModel):
    full_name: str
    birth_date: date

class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    publication_date: date

class Book(BookBase):
    id: int
    class Config:
        orm_mode = True

class GenreBase(BaseModel):
    name: str
    parent_id: int = None

class Genre(GenreBase):
    id: int

    class Config:
        orm_mode = True
