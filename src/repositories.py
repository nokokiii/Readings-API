from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Define the connection string
connection_string = os.getenv('connection_string')

# Create an engine
engine = create_engine(connection_string)

# Now you can use this engine to interact with your database
