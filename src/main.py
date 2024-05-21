from flask import Flask, Response, jsonify, request
from controllers import add_book
from repositories import get_book_data
from sqlalchemy import create_engine, text
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

app = Flask(__name__)


class WLapi:
    def __init__(self):
        pass

    def ping(self):
        return "Elo zielo"
    
    def send_book(self, data):
        add_book(data)
        return Response(status=200)
        



api = WLapi()


@app.route('/')
def ping():
    return api.ping()


@app.post('/add_book')
def send_book():
    data = request.json()
    title, author_name, kind_name = get_book_data(data)
    api.send_book(title, author_name, kind_name)

@app.route('/get_book')
def get_book():  
    connection_string = os.getenv('connection_string')

    engine = create_engine(connection_string)

    with engine.connect() as con:
        query = """
        SELECT * FROM Books;
        """

    statement = text(query)

    result = con.execute(statement)
    print(result.fetchall())





if __name__ == "__main__":
    app.run(port=5001, debug=True)