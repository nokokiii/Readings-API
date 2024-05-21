from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from db.scheme import Base  # Import your Base model for creating the database schema
from controllers import book_bp  # Import the Blueprint

# Load environment variables
load_dotenv()

# Get the connection string from the environment variable
connection_string = os.getenv('connection_string')

# Create the engine
engine = create_engine(connection_string)

# Create the Flask app
app = Flask(__name__)

# Set the engine for the Blueprint
book_bp.engine = engine

# Register the Blueprint
app.register_blueprint(book_bp, url_prefix='/books')

# Define the ping route
@app.route('/')
def ping():
    return "jebac baltiona"

if __name__ == "__main__":
    # Create the database tables if they don't exist
    Base.metadata.create_all(engine)
    # Run the Flask app
    app.run(port=5001, debug=True)
