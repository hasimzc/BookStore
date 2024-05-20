from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    parent_id = Column(Integer, ForeignKey("genres.id"))

    parent = relationship("Genre", remote_side=[id])
    books = relationship("Book", secondary="book_genre", back_populates="genres")

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(255))
    birth_date = Column(Date)

    books = relationship("Book", secondary="book_author", back_populates="authors")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    publication_date = Column(Date)

    authors = relationship("Author", secondary="book_author", back_populates="books")
    genres = relationship("Genre", secondary="book_genre", back_populates="books")

class BookAuthor(Base):
    __tablename__ = "book_author"

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)

class BookGenre(Base):
    __tablename__ = "book_genre"

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)
