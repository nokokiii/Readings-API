import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

Base = declarative_base()

class Kind(Base):
    __tablename__ = 'kinds'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

def collect_kinds():
    r = requests.get("https://wolnelektury.pl/api/kinds/").json()
    kinds = [kind["name"] for kind in r]
    return kinds

def insert_kinds(kinds, session):
    for kind_name in kinds:
        existing_kind = session.query(Kind).filter_by(name=kind_name).first()
        if existing_kind is None:
            kind = Kind(name=kind_name)  
            session.add(kind)  
    session.commit()



def main():
    
    load_dotenv()
    
    DATABASE_URL = os.getenv('connection_string')

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    kinds = collect_kinds()
    insert_kinds(kinds, session)

    added_kinds = session.query(Kind).all()
    for kind in added_kinds:
        print(kind.name)

if __name__ == "__main__":
    main()
