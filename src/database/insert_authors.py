import os

import requests

from src.database.schema import Author
from src.database.db import create_session


def collect_authors():
    r = requests.get("https://wolnelektury.pl/api/authors/").json()
    return [author["name"] for author in r]


def insert_authors(authors, session):
    for author_name in authors:
        existing_author = session.query(Author).filter_by(name=author_name).first()
        if existing_author is None:
            author = Author(name=author_name)  
            session.add(author)  
    session.commit()


def main():
    session = create_session()

    authors = collect_authors()
    insert_authors(authors, session)

    added_authors = session.query(Author).all()

    for author in added_authors:
        print(author.name)

if __name__ == "__main__":
    main()
