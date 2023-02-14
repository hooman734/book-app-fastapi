from typing import Union, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid


class Book(BaseModel):
    id: Union[str, None] = None
    title: str
    description: Optional[str]

books = []

app = FastAPI()

# Welcome Note
@app.get("/")
async def root():
    return { "message": "Welcome to my Book App API" }

# Get all books
@app.get("/api/v1/books")
async def show_all():
    return { "all_books": books }

# Get a book by ID - path
@app.get("/api/v1/book/{id}")
async def show_by_id(id: str):
    for book in books:
        if str(book.id) == str(id):
            return { "requested_book": book }
    raise HTTPException(404, f"Book with ID: {id} not found!")

# Get a book by ID - query parameter
@app.get("/api/v1/book")
async def show_by_id_query(id: str):
    for book in books:
        if str(book.id) == str(id):
            return { "requested_book": book }
    raise HTTPException(404, f"Book with ID: {id} not found!")

# Add new book
@app.post("/api/v1/book")
async def add_book(new_book: Book):
    if new_book.id == None:
        new_book.id = uuid.uuid4().hex
        books.append(new_book)
        return { "added_book": new_book }
    raise HTTPException(418, f"You are not allowed to specify an ID")

# Delete a book
@app.delete("/api/v1/book/{id}")
async def delete_by_id(id: str):
    for book in books:
        if str(book.id) == str(id):
            books.remove(book)
            return { "deleted_book": book }
    raise HTTPException(404, f"Book with ID: {id} not found!")

# Edit a book - just title with query parameter
@app.patch("/api/v1/book/{id}")
async def edit_by_id(id: str, new_title: str):
    for book in books:
        if str(book.id) == str(id):
            book.title = new_title
            return { "edited_book": book }
    raise HTTPException(404, f"Book with ID: {id} not found!")

# Edit a book - just description with query parameter
@app.patch("/api/v1/book/{id}")
async def edit_by_id(id: str, new_description: str):
    for book in books:
        if str(book.id) == str(id):
            book.description = new_description
            return { "edited_book": book }
    raise HTTPException(404, f"Book with ID: {id} not found!")

# Edit a book - just title with query parameter
@app.put("/api/v1/book/{id}")
async def edit_by_id(id: str, new_book: Book):
    for book in books:
        if str(book.id) == str(id):
            books.remove(book)
            new_book.id = id
            books.append(new_book)
            return { "edited_book": new_book }
    raise HTTPException(404, f"Book with ID: {id} not found!")

