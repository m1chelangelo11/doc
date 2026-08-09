import io
import os
from typing import Any

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from markitdown import MarkItDown
from pydantic import BaseModel

from .openrouter import send_query


class RequestContent(BaseModel):
    content: list[dict[str, Any]]


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

md = MarkItDown()


@app.post("/query")
async def query(request_content: RequestContent):
    result = send_query(request_content.content)
    return result


@app.post("/parse_file")
async def parse_file(file: UploadFile):
    file_bytes = await file.read()
    binary_stream = io.BytesIO(file_bytes)

    _, extension = os.path.splitext(file.filename)
    extension = extension.lower()

    try:
        result = md.convert_stream(binary_stream, file_extension=extension)
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Wrong file type")

    if result.text_content.strip() == "":
        raise HTTPException(status_code=400, detail="Empty file")

    parsed_file = {
        "filename": file.filename,
        "filetype": file.content_type,
        "filedata": result.text_content,
    }

    return parsed_file
