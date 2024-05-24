from fastapi import Depends

from src.database.db import Database, db_provider
from src.app.models import Book
from src.database.schema import Author, Kind


class Logic:
    def __init__(self, db: Database):
        self.db = db


    def add_book(self, book_params: Book) -> tuple[str, dict]:
        """
        Insert a book into the database.
        """
        try:
            author = self.db.is_author(book_params.author)
            if not author:
                author = Author(name=book_params.author)
                self.db.add_author(author)

            kind = self.db.is_kind(book_params.kind)
            if not kind:
                kind = Kind(name=book_params.kind)
                self.db.add_kind(kind)

            self.db.add_book(book_params.title, author.id, kind.id)
            return "Created", {"msg": "Book created successfully"}
        except Exception as e:
            self.db.rollback()
            print(e)
            return "Error", {"msg": "There was an error", "error": str(e)}


    def get_book(self, title: str) -> tuple[str, dict]:
        """
        Get a book from the database by title.
        """        
        if book := self.db.get_book(title):
            return "Found", book.get_dict()
        else:
            return "Not Found", {"msg": "Book not found"}
        

    def get_books(self, params: dict):
        """
        Get books from the database by title, author, or kind.
        """
        try:
            if books := self.db.get_books(params):
                return "OK", books
            else:
                return "Not Found", {"msg": "No books found"}
        except Exception as e:
            print(e)
            return "Error", {"msg": "Something went wrong"}


def logic_provider(db: Database = Depends(db_provider)) -> Logic:
    return Logic(db)
