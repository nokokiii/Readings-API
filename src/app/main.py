from typing import Annotated

import uvicorn
from fastapi import FastAPI, Path, Response, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.app.logic import Logic, logic_provider
from src.app.models import *


app = FastAPI(
    title="WLapi",
    description="A simple API to manage books",
    version="0.1"
)


@app.post("/book")
def add_book(
    book: Book = Depends(),
    logic: Logic = Depends(logic_provider)
) -> Response:
    """
    This enpdpoint is used to add a book to the database
    """
    status_msg, res = logic.add_book(book_params=book)

    if status_msg == "Created":
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=res)
    elif status_msg == "Error":
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res)


@app.get("/book/{title}")
def get_book(
    title: Annotated[str, Path(title="The title of the book", ge=1, le=1000)],
    logic: Logic = Depends(logic_provider)
) -> Response:
    """
    This endpoint is used to get a book from the database based on the title
    """
    status_msg, res = logic.get_book(title=title)

    if status_msg == "Found":
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))
    elif status_msg == "Not Found":
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
    

@app.get('/books')
def get_books(
    filters: Filters = Depends(),
    logic: Logic = Depends(logic_provider)
) -> Response:
    """
    This endpoint is used to get books from the database based on the filters
    
    """
    status_msg, res = logic.get_books(filters=filters)

    if status_msg == "OK":
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))
    elif status_msg == "Not Found":
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
