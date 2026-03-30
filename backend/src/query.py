from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from .openrouter import send_query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

class RequestContent(BaseModel):
    content: List[Dict[str, Any]]

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.post("/query")
async def query(request_content: RequestContent):
    result = send_query(request_content.content)
    return result
