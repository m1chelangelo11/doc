from fastapi import FastAPI
from pydantic import BaseModel
from openrouter import send_query

class RequestContent(BaseModel):
    content: str

app = FastAPI()

@app.post("/query")
async def uery(request_content: RequestContent):
    result = send_query(request_content.content)
    return result

