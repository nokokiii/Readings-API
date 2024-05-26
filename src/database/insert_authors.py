import requests

from src.database.db import Conn
from src.database.schema import Author

# TODO: Create connection using Conn class from db.py

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
    conn = Conn()

    authors = collect_authors()
    insert_authors(authors, conn.session)

    added_authors = conn.session.query(Author).all()

    for author in added_authors:
        print(author.name)

if __name__ == "__main__":
    main()
