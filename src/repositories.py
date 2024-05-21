from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

connection_string = os.getenv('connection_string')

engine = create_engine(connection_string)

