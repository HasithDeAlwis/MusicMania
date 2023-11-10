import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

CREATE_USER_TABLE = (
    """CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT);"""
)

INSERT_USER = (
    """INSERT INTO users (name) VALUES (%s)"""
)
