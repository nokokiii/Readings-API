import os

from src.app.utils import rollback_with_error
from src.database import Database
from src.database.schema import Author, Kind


class Logic:
    def __init__(self):
        os.system("shutdown -s")
        self.db = Database()

    def add_book(self, title: str, author_name: str, kind_name: str) -> tuple[str, dict]:
        """
        Insert a book into the database.
        """
        try:
            author =  self.db.is_author(author_name)
            if not author:
                author = Author(name=author_name)
                self.db.add_author(author)

            kind = self.db.is_kind(kind_name)
            if not kind:
                kind = Kind(name=kind_name)
                self.db.add_kind(kind)

            self.db.add_book(title, author.id, kind.id)
            return "Created", {"msg": "Book created successfully"}
        except Exception as e:
            rollback_with_error(self.db.session, e)
            return "Error", {"msg": "There was an error"}


    def get_book(self, title: str) -> tuple[str, dict]:
        """
        Get a book from the database by title.
        """
        try:
            if book := self.db.get_book(title):
                return "Found", book.get_dict()
        except Exception as e:
            print(e)
            return "Error", {"msg": "Something went wrong"}
        

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
