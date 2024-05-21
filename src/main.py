from flask import Flask, Response, jsonify, request
from controllers import add_book
from repositories import get_book_data
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from model import Author, Base, Kind
import os

load_dotenv()

connection_string = os.getenv('connection_string')

engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

app = Flask(__name__)

class WLapi:
    def __init__(self):
        pass

    def ping(self):
        return "Elo zielo"

    def send_book(self, title, author, kind):
        session = Session()
        try:
            existing_author = session.query(Author).filter_by(name=author).first()
            if existing_author:
                author_id = existing_author.id
            else:
                new_author = Author(name=author)
                session.add(new_author)
                session.commit()
                author_id = new_author.id

            existing_kind = session.query(Kind).filter_by(name=kind).first()
            if existing_kind:
                kind_id = existing_kind.id
            else:
                new_kind = Kind(kind=kind)
                session.add(new_kind)
                session.commit()
                kind_id = new_kind.id

            add_book(title, author_id, kind_id)
            session.close()
            return Response(status=200)
        except IntegrityError:
            session.rollback()
            existing_author = session.query(Author).filter_by(name=author).first()
            if existing_author:
                author_id = existing_author.id
            else:
                session.close()
                return Response(status=500, response="Failed to handle duplicate author error")

            existing_kind = session.query(Kind).filter_by(kind=kind).first()
            if existing_kind:
                kind_id = existing_kind.id
            else:
                session.close()
                return Response(status=500, response="Failed to handle duplicate kind error")

            add_book(title, author_id, kind_id)
            session.close()
            return Response(status=200)


api = WLapi()

@app.route('/')
def ping():
    return api.ping()

@app.post('/books/add_book')
def append_book():
    try:
        data = request.get_json()
        title, author, kind = get_book_data(data)
        api.send_book(title, author, kind)
        return Response(status=200)
    except Exception as e:
        print(f"Error: {e}")
        return Response(status=500, response=str(e))

@app.route('/get_book')
def get_book():
    try:
        with engine.connect() as con:
            query = "SELECT * FROM Books"
            statement = text(query)
            result = con.execute(statement)
            columns = result.keys()
            
            books = [dict(zip(columns, row)) for row in result]
            
            return jsonify(books)
    except Exception as e:
        print(f"Error: {e}")
        return Response(status=500, response=str(e))


if __name__ == "__main__":
    app.run(port=5001, debug=True)
