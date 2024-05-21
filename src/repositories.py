from sqlalchemy.orm import Session
from db.scheme import Author, Epoch, Genre, Kind, Book

class AuthorRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create(self, name: str):
        author = self.session.query(Author).filter_by(name=name).first()
        if not author:
            author = Author(name=name)
            self.session.add(author)
            self.session.commit()
        return author

class EpochRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create(self, name: str):
        epoch = self.session.query(Epoch).filter_by(name=name).first()
        if not epoch:
            epoch = Epoch(name=name)
            self.session.add(epoch)
            self.session.commit()
        return epoch

class GenreRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create(self, name: str):
        genre = self.session.query(Genre).filter_by(name=name).first()
        if not genre:
            genre = Genre(name=name)
            self.session.add(genre)
            self.session.commit()
        return genre

class KindRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create(self, name: str):
        kind = self.session.query(Kind).filter_by(name=name).first()
        if not kind:
            kind = Kind(name=name)
            self.session.add(kind)
            self.session.commit()
        return kind

class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_book(self, title: str, author: Author, epoch: Epoch, genre: Genre, kind: Kind):
        new_book = Book(title=title, author=author, epoch=epoch, genre=genre, kind=kind)
        self.session.add(new_book)
        self.session.commit()
        return new_book
