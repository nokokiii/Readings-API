from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from model import Base, Book

load_dotenv()


connection_str = os.getenv('connection_string')

engine = create_engine(connection_str)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


def add_book(title: str, author_id: int, kind_id: int) -> None:
    session = Session()
    try:
        book = Book(
            title=title,
            author_id=author_id,
            kind_id=kind_id
        )


        session.add(book)
        session.commit()
        print(f'Book "{title}" added successfully!')

    except Exception as e:
        session.rollback()
        print(e)   

    finally:
        session.close()

