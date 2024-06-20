from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def get_embeddings_for_chunks(chunks, model="text-embedding-3-small"):
    client = OpenAI()
    embeddings = []
    for chunk in chunks:
        response = get_embedding(chunk)
        embeddings.append(response)
    return embeddings

def generate_response(messages):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        top_p=0.2,
        temperature=0.2)
    return completion.choices[0].message.content
