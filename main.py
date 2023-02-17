from typing import Optional, Union

from fastapi import FastAPI, HTTPException, Depends
import uuid
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal

from book import Book

BOOKS = []

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Welcome to Note
@app.get("/")
async def root():
    return {"message": "Welcome to my Book App API"}


# Get all books
@app.get("/api/v1/books")
async def show_all(db: Session = Depends(get_db)):
    return {"all_books": BOOKS}


# Get a book by ID - path
@app.get("/api/v1/book/{book_id}")
async def show_by_id(book_id: str):
    for book in BOOKS:
        if str(book.id) == str(book_id):
            return {"requested_book": book}
    raise HTTPException(404, f"Book with ID: {book_id} not found!")


# Get a book by ID - query parameter
@app.get("/api/v1/book")
async def show_by_id_query(book_id: str):
    for book in BOOKS:
        if str(book.id) == str(book_id):
            return {"requested_book": book}
    raise HTTPException(404, f"Book with ID: {book_id} not found!")


# Add new book
@app.post("/api/v1/book")
async def add_book(new_book: Book):
    if new_book.id is None:
        new_book.id = uuid.uuid4().hex
        BOOKS.append(new_book)
        return {"added_book": new_book}
    raise HTTPException(418, f"You are not allowed to specify an ID! retry without having an ID field.")


# Delete a book
@app.delete("/api/v1/book/{book_id}")
async def delete_by_id(book_id: str):
    for book in BOOKS:
        if str(book.id) == str(book_id):
            BOOKS.remove(book)
            return {"deleted_book": book}
    raise HTTPException(404, f"Book with ID: {book_id} not found!")


# Edit a book - with query parameter
@app.patch("/api/v1/book/{book_id}")
async def edit_by_id(book_id: str,
                     new_title: Union[str, None] = None,
                     new_description: Union[str, None] = None,
                     new_rating: Union[int, None] = None):
    for book in BOOKS:
        if str(book.id) == str(book_id):
            if new_title:
                book.title = new_title
            if new_description:
                book.description = new_description
            if new_rating:
                book.rating = new_rating
            return {"edited_book": book}
    raise HTTPException(404, f"Book with ID: {book_id} not found!")


# Edit a book - with body
@app.put("/api/v1/book/{book_id}")
async def edit_by_id(book_id: str, new_book: Book):
    for book in BOOKS:
        if str(book.id) == str(book_id):
            BOOKS.remove(book)
            new_book.id = book_id
            BOOKS.append(new_book)
            return {"edited_book": new_book}
    raise HTTPException(404, f"Book with ID: {book_id} not found!")
