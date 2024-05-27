from typing import List, Tuple

from fastapi import Depends

from src.app.models import Book
from src.database.db import Database, db_provider
from src.database.schema import Author, Kind


class Logic:
    """
    This class contains the business logic for the application.
    """

    def __init__(self, db: Database):
        self.db = db

    def create_author(self, author: str) -> Author:
        """
        Create an author in the database if it doesn't exist.
        """
        author = self.db.is_author(author)

        if not author:
            author = Author(name=author)
            self.db.add_author(author)

        return author

    
    def create_kind(self, kind: str) -> Kind:
        """
        Create a kind in the database if it doesn't exist.
        """
        kind = self.db.is_kind(kind)

        if not kind:
            kind = Kind(name=kind)
            self.db.add_kind(kind)

        return kind


    def add_book(self, book_params: Book) -> Tuple[str, dict]:
        """
        Insert a book into the database.
        """
        try:
            author = self.create_author(book_params.author)
            kind = self.create_kind(book_params.kind)

            self.db.add_book(book_params.title, author.id, kind.id)
            return "Created", {"msg": "Book created successfully"}
        except Exception as e:
            self.db.rollback()
            print(e)
            return "Error", {"msg": "There was an error", "error": str(e)}


    def get_book(self, title: str) -> Tuple[str, dict]:
        """
        Get a book from the database by title.
        """        
        if book := self.db.get_book(title):
            return "Found", book.get_dict()
        else:
            return "Not Found", {"msg": "Book not found"}
        

    def get_books(self, authors: List[str], kinds: List[str]) -> Tuple[str, dict]:
        """
        Get books from the database by title, author, or kind.
        """
        try:
            if books := self.db.get_books(authors, kinds):
                return "OK", books
            else:
                return "Not Found", {"msg": "No books found"}
        except Exception as e:
            print(e)
            return "Error", {"msg": "Something went wrong"}


def logic_provider(db: Database = Depends(db_provider)) -> Logic:
    """
    Return an instance of the Logic class.
    """
    return Logic(db)
