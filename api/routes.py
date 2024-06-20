from fastapi import APIRouter, UploadFile, File
from api.controller import handle_chat, handle_upsert, handle_delete, handle_index, handle_query

router = APIRouter()

@router.post("/chat")
async def chat(query: str):
    return await handle_chat(query)

@router.post("/query")
async def query(query: str):
    return await handle_query(query)

@router.post("/upsert")
async def upsert(file: UploadFile = File(...)):
    return await handle_upsert(file)

@router.delete("/delete")
async def delete(file_name: str):
    return await handle_delete(file_name)

@router.post("/index")
async def index():
    return await handle_index()

@router.get("/")
async def root():
    return {"message": "Welcome to the API. Use the endpoints /chat, /upsert, /delete, and /index for respective functionalities."}