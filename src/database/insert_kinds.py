import requests

from src.database.db import Conn
from src.database.schema import Kind

# TODO: Create connection using Conn class from db.py


def collect_kinds():
    r = requests.get("https://wolnelektury.pl/api/kinds/").json()
    return [kind["name"] for kind in r]


def insert_kinds(kinds, session):
    for kind_name in kinds:
        existing_kind = session.query(Kind).filter_by(name=kind_name).first()
        if existing_kind is None:
            kind = Kind(name=kind_name)  
            session.add(kind)  
    session.commit()


def main():
    conn = Conn()

    kinds = collect_kinds()
    insert_kinds(kinds, conn.session)

    added_kinds = conn.session.query(Kind).all()
    
    for kind in added_kinds:
        print(kind.name)

if __name__ == "__main__":
    main()
