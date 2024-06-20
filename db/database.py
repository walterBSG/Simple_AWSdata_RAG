import psycopg2
import os

def get_connection():
    conn_string = os.getenv('DATABASE_URL')
    return psycopg2.connect(conn_string)