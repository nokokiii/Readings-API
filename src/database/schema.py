from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)  
    name = Column(String, unique=True, nullable=False)


class Kind(Base):
    __tablename__ = 'kinds'
    id = Column(Integer, primary_key=True, autoincrement=True)  
    name = Column(String, unique=True, nullable=False)


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    kind_id = Column(Integer, ForeignKey('kinds.id'), nullable=False)

    def get_dict(self) -> dict:
        book_dict = self.__dict__
        book_dict.pop('_sa_instance_state')
        return book_dict
