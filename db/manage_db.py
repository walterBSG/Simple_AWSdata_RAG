import math
import numpy as np
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector

def add_file(conn, filename, chunks, embeddings):
    data_list = [(filename, chunk, embedding) for chunk, embedding in zip(chunks, embeddings)]
    
    cur = conn.cursor()
    try:
        # Delete existing records with the same filename
        cur.execute("DELETE FROM documents WHERE name = %s", (filename,))
        
        # Insert new records
        execute_values(cur, "INSERT INTO documents (name, content, embedding) VALUES %s", data_list)
        
        # Commit the transaction
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback the transaction in case of error
        conn.rollback()
    finally:
        # Close the cursor
        cur.close()


def remove_file(conn, filename):
    cur = conn.cursor()
    try:
        # Delete the records with the given filename
        cur.execute("DELETE FROM documents WHERE name = %s", (filename,))
        
        # Commit the transaction
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback the transaction in case of error
        conn.rollback()
    finally:
        # Close the cursor
        cur.close()


def build_index(conn):
    # Get the number of records from the documents table
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM documents;')
    num_records = cur.fetchone()[0]
    
    #calculate the index parameters according to best practices
    num_lists = num_records / 1000
    if num_lists < 10:
        num_lists = 10
    if num_records > 1000000:
        num_lists = math.sqrt(num_records)

    #use the cosine distance measure, which is what we'll later use for querying
    cur.execute(f'CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = {num_lists});')
    conn.commit()

def get_similar_docs(conn, query_embedding):
    # Register pgvector extension
    register_vector(conn)
    cur = conn.cursor()
    
    # Get the top 5 most similar documents using the KNN <=> operator
    cur.execute("SELECT content FROM documents ORDER BY embedding <=> %s::vector LIMIT 10", (query_embedding,))
    top_docs = cur.fetchall()
    return top_docs