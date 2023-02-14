from typing import Union, NewType
from fastapi import FastAPI
from pydantic import BaseModel
import uuid


class Book(BaseModel):
    title: str
    id: Union[str, None] = None

books = []

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Welcome to my Book App API"}

@app.get("/api/v1/books")
async def show_all():
    return books

@app.get("/api/v1/book/{id}")
async def show_by_id(id: str):
    result = None
    for book in books:
        if str(book.id) == str(id):
            result = book
    return result

@app.post("/api/v1/book")
async def add_book(new_book: Book):
    resul = None
    if new_book.id == None:
        new_book.id = uuid.uuid4().hex
        books.append(new_book)
        result = new_book
    return result

@app.delete("/api/v1/book/{id}")
async def delete_by_id(id: str):
    result = None
    for book in books:
        if str(book.id) == str(id):
            result = book
            books.remove(result)
    return result

@app.put("/api/v1/book/{id}")
async def edit_by_id(id: str, new_title: str):
    result = None
    for book in books:
        if str(book.id) == str(id):
            result = book
            book.title = new_title
    return result
