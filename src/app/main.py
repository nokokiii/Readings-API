"""
This module contains the main FastAPI application
"""

from typing import Annotated, List

from fastapi import FastAPI, Response, status, HTTPException, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.app.logic import Logic, logic_provider
from src.app.models import Book


app = FastAPI(
    title="WLapi",
    description="A simple API to manage books",
    version="1.0"
)


@app.post("/book")
def add_book(
    book: Book = Depends(),
    logic: Logic = Depends(logic_provider)
) -> Response:
    """
    This enpdpoint is used to add a book to the database
    """
    _, res = logic.add_book(book_params=book)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=res)


@app.get("/book/{title}")
def get_book(
    title: str = Annotated[str, Query(...)],
    logic: Logic = Depends(logic_provider)
) -> Response:
    """
    This endpoint is used to get a book from the database based on the title
    """
    status_msg, res = logic.get_book(title=title)

    if status_msg == "Found":
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))
    elif status_msg == "Not Found":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
    

@app.get('/books')
def get_books(
    authors: List[str] = Query([]),
    kinds: List[str] = Query([]),
    logic: Logic = Depends(logic_provider)
) -> Response:
    """
    This endpoint is used to get books from the database based on the filters
    """
    status_msg, res = logic.get_books(authors=authors, kinds=kinds)

    if status_msg == "OK":
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))
    elif status_msg == "Not Found":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
