import io
import os
import tempfile
from typing import Any

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from llama_index.core import SimpleDirectoryReader
from markitdown import MarkItDown
from pydantic import BaseModel

from .openrouter import send_query
from .vectorstore import add_to_collection


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
    if file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Image uploading is not supported")

    file_bytes = await file.read()
    binary_stream = io.BytesIO(file_bytes)

    _, extension = os.path.splitext(file.filename)
    extension = extension.lower()

    text_content = ""

    try:
        if file.content_type == "application/pdf" or extension == ".pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(file_bytes)
                tmp_path = tmp_file.name

            try:
                documents = SimpleDirectoryReader(input_files=[tmp_path]).load_data()

                text_content = "\n".join([doc.text for doc in documents])
                
            finally:
                os.remove(tmp_path)

        elif file.content_type.startswith("application/vnd.openxmlformats-officedocument") or extension in [".docx", ".xlsx", ".pptx"]:
            result = md.convert_stream(binary_stream, file_extension=extension)
            text_content = result.text_content

        elif file.content_type.startswith("text/") or extension in [".md", ".txt", ".html", ".csv", ".json"]:
            text_content = file_bytes.decode()

        else:
            raise ValueError(f"Unsupported file extension: {extension}")

    except ValueError:
        raise HTTPException(status_code=400, detail="Wrong file type")
    except Exception as e: # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {e!s}")

    if not text_content or text_content.strip() == "":
        raise HTTPException(status_code=400, detail="Empty file or no readable text found")

    file_uuid = add_to_collection(text_content, file.filename)


    return {"filename": file.filename,
            "file_uuid": file_uuid}
