from pydantic import BaseModel
from datetime import date

class AuthorBase(BaseModel):
    full_name: str
    birth_date: date

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    full_name: str = None
    birth_date: date = None

class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    publication_date: date

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: str = None
    publication_date: date = None

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True