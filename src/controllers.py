from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from model import Base, Author, Kind, Book

from repositories import get_book_data

load_dotenv()

connection_string = os.getenv('connection_string')

engine = create_engine(connection_string)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

def add_book(title: str, author_name: str, kind_name: str) -> None:
    session = Session()
    
    try:
        author = session.query(Author).filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            session.add(author)
            session.commit()

        kind = session.query(Kind).filter_by(name=kind_name).first()
        if not kind:
            kind = Kind(name=kind_name)
            session.add(kind)
            session.commit()

            
        book = Book(
            title=title,
            author_id=author.id,
            kind_id=kind.id
        )

        session.add(book)

        session.commit()

        print(f'Book "{title}" added successfully!')

    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")

    finally:
        session.close()