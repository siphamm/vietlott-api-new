import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    conn = psycopg2.connect(database=os.environ["POSTGRES_DB_NAME"],
                            host=os.environ["POSTGRES_HOST"],
                            user=os.environ["POSTGRES_USER"],
                            password=os.environ["POSTGRES_PASSWORD"])
    return conn
