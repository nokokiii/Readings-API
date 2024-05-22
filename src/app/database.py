import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import Author, Kind, Book, Base


def create_session() -> sessionmaker:
    """
    Create a session to interact with the database.
    """
    load_dotenv()
    connection_string = os.getenv('connection_string')
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


class Database:
    def __init__(self):
        self.session = create_session()

    def rollback(self) -> None:
        """
        Rollback the session.
        """
        self.session.rollback()

    def is_author(self, author: str) -> Author | None:
        """
        Checks if an author already exists in the database. If yes returns the author.
        """
        return self.session.query(Author).filter_by(name=author).first()
    
    def is_kind(self, kind: str) -> Kind | None:
        """
        Check if a kind already exists in the database. If yes returns the kind.
        """
        return self.session.query(Kind).filter_by(name=kind).first()
    
    def add_author(self, author: Author) -> None:
        """
        Adds an author to the database.
        """
        try:
            self.session.add(author)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)


    def add_kind(self, kind: Kind) -> None:
        """
        Adds a kind to the database.
        """
        try:
            self.session.add(kind)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)

    
    def add_book(self, title: str, author_id: int, kind_id: int) -> None:
        """
        Adds a book to the database.
        """
        try:
            book = Book(title=title, author_id=author_id, kind_id=kind_id)

            self.session.add(book)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)


    def get_book(self, title: str) -> Book | None:
        """
        Get a book from the database.
        """
        return self.session.query(Book).filter_by(title=title).first()
