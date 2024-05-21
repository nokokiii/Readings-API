from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from db.scheme import Base  # Import your Base model for creating the database schema
from controllers import book_bp  # Import the Blueprint

load_dotenv()

connection_string = os.getenv('connection_string')

engine = create_engine(connection_string)

app = Flask(__name__)

book_bp.engine = engine

app.register_blueprint(book_bp, url_prefix='/books')


@app.route('/')
def ping():
    return "jebac baltiona"


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(port=5001, debug=True)
