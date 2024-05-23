# Book Store API

Welcome to the Book Store API! This is a RESTful API built using FastAPI, SQLAlchemy, and SQLite. The API allows you to manage books, authors, and genres in a bookstore.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Schemas](#schemas)
- [Contribution](#contribution)
- [License](#license)

## Overview

The Book Store API provides endpoints to create, read, update, and delete books, authors, and genres. It also supports associations between books and authors, and books and genres.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed on your local machine
- Access to a terminal or command-line interface
- Basic understanding of Python and FastAPI

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/bookstore-api.git
    cd bookstore-api
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```bash
    uvicorn main:app --reload
    ```

## Usage

To interact with the API, you can use tools like [curl](https://curl.se/), [Postman](https://www.postman.com/), or any other API client.

Visit `http://127.0.0.1:8000/docs` to access the interactive API documentation provided by Swagger.

## API Endpoints

Here are some of the main endpoints available in the API:

- **Authors**:
  - `GET /authors/` - List all authors
  - `POST /authors/` - Create a new author
  - `GET /authors/{author_id}/books` - Get books by a specific author

- **Books**:
  - `GET /books/` - List all books
  - `POST /books/` - Create a new book
  - `GET /books/{book_id}` - Get a specific book
  - `PUT /books/{book_id}` - Update a specific book
  - `DELETE /books/{book_id}` - Delete a specific book

- **BookAuthors**:
  - `POST /book_authors/{book_id}/add_authors` - Add authors to a book

- **Genres**:
  - `GET /genres/` - List all genres
 
- **BookGenres**:
  - `POST /book_genres/{book_id}/add_genres` - Add genres to a book
  - `GET /book_genres/genre/{genre_name}/books` - List books by genre

Refer to the interactive API documentation at `http://127.0.0.1:8000/docs` for a complete list of endpoints and their descriptions.

## Database Models

The database models are defined using SQLAlchemy in the `db_models.py` file:

- **Author**: Represents an author with fields `id`, `full_name`, and `birth_date`.
- **Book**: Represents a book with fields `id`, `title`, and `publication_date`.
- **Genre**: Represents a genre with fields `id`, `name`, and `parent_id`.

Additionally, there are association tables to manage many-to-many relationships between books and authors, and books and genres.

## Schemas

Pydantic models are used for request validation and response formatting, defined in the `schemas.py` file:

- **AuthorCreate**: Schema for creating a new author.
- **Author**: Schema for returning author data.
- **BookCreate**: Schema for creating a new book.
- **Book**: Schema for returning book data.
- **GenreResponse**: Schema for returning genre data.
- **GenreDetails**: Schema for returning detailed genre data.

## Contribution

If you would like to contribute to this project, please follow these steps:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make the necessary changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for using the Book Store API! If you have any questions or suggestions, please open an issue or contribute directly to the project.
