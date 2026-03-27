from fastapi import FastAPI
from pydantic import BaseModel
from openrouter import send_query
from fastapi.middleware.cors import CORSMiddleware

class RequestContent(BaseModel):
    content: str

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

