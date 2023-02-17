from typing import Union
from fastapi import FastAPI, HTTPException, Depends
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
    return {"all_books": db.query(models.Books).all()}


# Get a book by ID - path
@app.get("/api/v1/book/{book_id}")
async def show_by_id(book_id: str, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(book_id == models.Books.id).first()
    if book_model is None:
        raise HTTPException(404, f"Book with ID: {book_id} not found!")
    requested_book = Book(title=book_model.title, description=book_model.description, rating=book_model.rating)
    return {"requested_book": {"id": book_id, **dict(requested_book)}}


# Get a book by ID - query parameter
@app.get("/api/v1/book")
async def show_by_id_query(book_id: str, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(book_id == models.Books.id).first()
    if book_model is None:
        raise HTTPException(404, f"Book with ID: {book_id} not found!")
    requested_book = Book(title=book_model.title, description=book_model.description, rating=book_model.rating)
    return {"requested_book": {"id": book_id, **dict(requested_book)}}


# Add new book
@app.post("/api/v1/book")
async def add_book(new_book: Book, db: Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = new_book.title
    book_model.description = new_book.description
    book_model.rating = new_book.rating

    db.add(book_model)
    db.commit()

    return {"added_book": {"id": book_model.id, **dict(new_book)}}


# Delete a book
@app.delete("/api/v1/book/{book_id}")
async def delete_by_id(book_id: str, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(book_id == models.Books.id).first()
    if book_model is None:
        raise HTTPException(404, f"Book with ID: {book_id} not found!")
    deleted_book = Book(title=book_model.title, description=book_model.description, rating=book_model.rating)
    db.query(models.Books).filter(book_id == models.Books.id).delete()
    db.commit()
    return {"deleted_book": {"id": book_id, **dict(deleted_book)}}


# Edit a book - with query parameter
@app.patch("/api/v1/book/{book_id}")
async def edit_by_id(book_id: str,
                     new_title: Union[str, None] = None,
                     new_description: Union[str, None] = None,
                     new_rating: Union[int, None] = None,
                     db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(book_id == models.Books.id).first()
    if book_model is None:
        raise HTTPException(404, f"Book with ID: {book_id} not found!")

    if new_title:
        book_model.title = new_title
    if new_description:
        book_model.description = new_description
    if new_rating:
        book_model.rating = new_rating

    edited_book = Book(title=book_model.title, description=book_model.description, rating=book_model.rating)
    db.add(book_model)
    db.commit()

    return {"edited_book": {"id": book_id, **dict(edited_book)}}


# Edit a book - with body
@app.put("/api/v1/book/{book_id}")
async def edit_by_id(book_id: str, new_book: Book, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(book_id == models.Books.id).first()
    if book_model is None:
        raise HTTPException(404, f"Book with ID: {book_id} not found!")
    book_model.title = new_book.title
    book_model.title = new_book.title
    book_model.description = new_book.description
    book_model.rating = new_book.rating

    db.add(book_model)
    db.commit()
    return {"edited_book": {"id": book_id, **dict(new_book)}}
