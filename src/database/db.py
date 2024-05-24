import os

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

    def is_author(self, author: str) -> Author | None:
        """
        Checks if an author already exists in the database. If yes returns the author.
        """
        return self.conn.session.query(Author).filter_by(name=author).first()
    
    def is_kind(self, kind: str) -> Kind | None:
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


    def get_book(self, title: str) -> Book | None:
        """
        Get a book from the database.
        """
        return self.conn.session.query(Book).filter_by(title=title).first()


    def get_books(self, params: dict) -> list[dict]:
        """
        Get books from the database based on the parameters.
        """
        author_name = params.get("author")
        kinds = params.get("kind")

        query = self.conn.query(Book)

        if author_name:
            if author := self.conn.session.query(Author).filter_by(name=author_name).first():
                query = query.filter_by(author_id=author.id)

        if kinds:
            kind_ids = []
            for kind in kinds:
                if kind_obj := self.conn.session.query(Kind).filter_by(name=kind).first():
                    kind_ids.append(kind_obj.id)

            if kind_ids:
                query = query.filter(Book.kind_id.in_(kind_ids))

        books = query.all()

        result = []
        for book in books:
            author = self.conn.session.query(Author).filter_by(id=book.author_id).first()
            kind = self.conn.session.query(Kind).filter_by(id=book.kind_id).first()
            result.append({
                'id': book.id,
                'title': book.title,
                'author': author.name if author else None,
                'kind': kind.name if kind else None,
            })

        return result


def conn_provider() -> Conn:
    return Conn()


def db_provider(conn: Conn = Depends(conn_provider)) -> Database:
    return Database(conn)
