import os
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from src.database.schema import Author, Kind, Book, Base


class Conn:
    """
    This Singleton class is used to create a connection to the database
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Conn, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        load_dotenv()
        connection_string = os.getenv('connection_string')
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        self.__initialized = True


class Database:
    def __init__(self, conn: Conn):
        self.conn = conn

    def rollback(self) -> None:
        """
        Rollback the session.
        """
        self.conn.session.rollback()

    def is_author(self, author: str) -> Optional[Author]:
        """
        Checks if an author already exists in the database. If yes returns the author.
        """
        return self.conn.session.query(Author).filter_by(name=author).first()
    
    def is_kind(self, kind: str) -> Optional[Kind]:
        """
        Check if a kind already exists in the database. If yes returns the kind.
        """
        return self.conn.session.query(Kind).filter_by(name=kind).first()
    
    def add_author(self, author: Author) -> None:
        """
        Adds an author to the database.
        """
        try:
            self.conn.session.add(author)
            self.conn.session.commit()
        except Exception as e:
            self.conn.session.rollback()
            print(e)


    def add_kind(self, kind: Kind) -> None:
        """
        Adds a kind to the database.
        """
        try:
            self.conn.session.add(kind)
            self.conn.session.commit()
        except Exception as e:
            self.conn.session.rollback()
            print(e)

    
    def add_book(self, title: str, author_id: int, kind_id: int) -> None:
        """
        Adds a book to the database.
        """
        try:
            book = Book(title=title, author_id=author_id, kind_id=kind_id)

            self.conn.session.add(book)
            self.conn.session.commit()
        except Exception as e:
            self.conn.session.rollback()
            print(e)


    def get_book(self, title: str) -> Optional[Book]:
        """
        Get a book from the database.
        """
        return self.conn.session.query(Book).filter_by(title=title).first()


    def get_books(self, authors: List[str], kinds: List[str]) -> List[dict]:
        """
        Get books from the database based on the parameters.
        """
        if authors and kinds:
            db_res = select(Book).join(Author).join(Kind).where(Author.name.in_(authors)).where(Kind.name.in_(kinds))
        elif authors:
            db_res = select(Book).join(Author).where(Author.name.in_(authors))
        elif kinds:
            db_res = select(Book).join(Kind).where(Kind.name.in_(kinds))
        else:
            db_res = select(Book)

        db_res = self.conn.session.execute(db_res).scalars().all()

        print(db_res)

        return db_res


def conn_provider() -> Conn:
    return Conn()


def db_provider(conn: Conn = Depends(conn_provider)) -> Database:
    return Database(conn)
