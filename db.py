#from decouple import config
from sqlalchemy import create_engine, select, Column, Integer, Text, Date, Float, ForeignKey
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session, declarative_base, relationship

# Load environment variables from .env file
load_dotenv()
# Retrieve database credentials from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Create the database URL
database_url = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

postgres_engine = create_engine(database_url,echo=True)
