from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Category_Base(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Category(Category_Base):
    __tablename__ = 'categories'


class Author(Category_Base):
    __tablename__ = 'authors'


class Epoch(Category_Base):
    __tablename__ = 'epochs'


class Genre(Category_Base):
    __tablename__ = 'genres'


class Kind(Category_Base):
    __tablename__ = 'kinds'


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    epoch_id = Column(Integer, ForeignKey('epochs.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    kind_id = Column(Integer, ForeignKey('kinds.id'))

    author = relationship("Author")
    epoch = relationship("Epoch")
    genre = relationship("Genre")
    kind = relationship("Kind")
