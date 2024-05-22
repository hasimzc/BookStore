from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Association Tables
book_author = Table('book_author', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True),
)

book_genre = Table('book_genre', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True),
)

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    birth_date = Column(Date)

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    publication_date = Column(Date)
    genres = relationship('Genre', secondary=book_genre, back_populates='books')

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey('genres.id'))

    books = relationship('Book', secondary=book_genre, back_populates='genres')
    subgenres = relationship('Genre', backref='parent', remote_side=[id])


# Database setup
DATABASE_URL = "sqlite:////Users/hasimzafercicek/desktop/bookstore.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
