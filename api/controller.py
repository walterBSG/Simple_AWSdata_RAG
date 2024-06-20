import os
import json
from fastapi import UploadFile
from utils.chunker import extract_text, chunk_text
from utils.openai_utils import get_embedding, generate_response, get_embeddings_for_chunks
from db.manage_db import add_file, remove_file, build_index, get_similar_docs
from db.database import get_connection
from dotenv import load_dotenv

load_dotenv()

async def handle_chat(messages: str):
    messages = json.loads(messages)
    last_message = messages[-1]
    embedding = get_embedding(last_message['content'])
    
    conn =  get_connection()
    docs = get_similar_docs(conn, embedding)
    
    #add system prompt
    system_prompt = os.getenv('SYSTEM_PROMPT')
    system_prompt += '\n\n'.join([doc[0] for doc in docs])
    system_prompt = {"role": "system", "content": system_prompt}
    temp_messages = messages.copy()
    temp_messages.insert(0, system_prompt)
    
    #add meta prompt in the last message
    last_message = f"Respond the question considering only the documentation provided:\n\nQuestion\n###\n{last_message['content']}\n###"
    last_message = {"role": "user", "content": last_message}
    temp_messages[-1] = last_message
    
    response = generate_response(temp_messages)
    
    print(system_prompt)
    messages.append({"role": "assistant", "content": response})
    #returning without system prompt and without meta prompt
    return {"response": messages}

async def handle_query(message: str):
    embedding = get_embedding(message)
    
    conn =  get_connection()
    docs = get_similar_docs(conn, embedding)
    
    #add system prompt
    messages = []
    system_prompt = os.getenv('SYSTEM_PROMPT')
    system_prompt += '\n\n'.join([doc[0] for doc in docs])
    system_prompt = {"role": "system", "content": system_prompt}
    messages.append(system_prompt)
    
    #add meta prompt in the last message
    message = f"Respond the question considering only the documentation provided:\n\nQuestion\n###\n{message}\n###"
    message = {"role": "user", "content": message}
    messages.append(message)
    
    response = generate_response(messages)
    return {"response": response}

async def handle_upsert(file: UploadFile):
    # Read the file content
    content = file.file.read()
    
    # Extract text from the file
    text = extract_text(content, file.filename)
    
    # Create the chunks of the files
    chunks = chunk_text(text)
        
    #Create the embeddings of the chunks
    embeddings = get_embeddings_for_chunks(chunks)
    
    # Create a new session
    conn = get_connection()
    
    # Add the file content and extracted text to the database
    add_file(conn, file.filename, chunks, embeddings)
    
    # Return the status and filename
    return {"status": "success", "filename": file.filename}

async def handle_delete(file_name: str):
    # Create a new session
    conn = get_connection()
    remove_file(conn, file_name)
    return {"status": "success", "filename": file_name}

async def handle_index():
    # Create a new session
    conn = get_connection()
    build_index(conn)
    return {"status": "success"}