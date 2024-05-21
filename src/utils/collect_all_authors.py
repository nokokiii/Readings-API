import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

def collect_authors():
    r = requests.get("https://wolnelektury.pl/api/authors/").json()
    authors = [author["name"] for author in r]
    return authors

def insert_authors(authors, session):
    for author_name in authors:
        existing_author = session.query(Author).filter_by(name=author_name).first()
        if existing_author is None:
            author = Author(name=author_name)  
            session.add(author)  
    session.commit()



def main():
    
    load_dotenv()
    
    DATABASE_URL = os.getenv('connection_string')

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    authors = collect_authors()
    insert_authors(authors, session)

    added_authors = session.query(Author).all()
    for author in added_authors:
        print(author.name)

if __name__ == "__main__":
    main()
