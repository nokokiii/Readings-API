from schema import Author, Kind
from database import Database

import os

class Logic:
    def __init__(self):
        self.db = Database()

    def ping(self):
        return "Elo zielo"

    def add_book(self, title: str, author_name: str, kind_name: str) -> tuple[str, dict]:
        try:
            if existing_author := self.db.is_author(author_name):   
                author = existing_author
            else:
                author = Author(name=author_name)
                self.db.add_author(author)

            if existing_kind := self.db.is_kind(kind_name):
                kind = existing_kind
            else:
                kind = Kind(name=kind_name)
                self.db.add_kind(kind)

            self.db.add_book(title, author.id, kind.id)
            return "Created", {"msg": "Book created successfully"}
        except Exception as e:
            self.db.session.rollback()
            print(e)
            return "Error", {"msg": "Something went wrong"}


    def get_book(self, title: str) -> tuple[str, dict]:
        try:
            book = self.db.get_book(title)
            return "Found", book.get_dict()
        except Exception as e:
            print(e)
            return "Error", {"msg": "Something went wrong"}


def getLogic():
    return Logic()
