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
from .vectorstore import add_to_collection, collection, delete_document, retrieve_chunks


class Message(BaseModel):
    role: str
    content: str | list[dict[str, Any]]

class RequestContent(BaseModel):
    messages: list[Message]
    use_rag: bool = False


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
    messages_list = [msg.model_dump() for msg in request_content.messages]

    if not messages_list:
        raise HTTPException(status_code=400, detail="Brak wiadomości w zapytaniu")

    if request_content.use_rag:
        last_message = messages_list[-1]
        last_user_text = ""

        if isinstance(last_message["content"], str):
            last_user_text = last_message["content"]

        elif isinstance(last_message["content"], list):
            for block in last_message["content"]:
                if block.get("type") == "text":
                    last_user_text = block.get("text", "")
                    break

        if collection.count() > 0:
            found_chunks = retrieve_chunks(query=last_user_text)

            if found_chunks:
                context_texts = []
                for chunk in found_chunks:
                    filename = chunk["metadata"].get("filename", "Unknown document")
                    context_texts.append(
                        f"--- Fragment of the document: {filename} ---\n{chunk['text']}"
                    )

                full_context = "\n\n".join(context_texts)

                system_prompt = (
                    "You are an AI assistant and teacher. Answer the user's questions based on "
                    "the fragments of the documents below. If there is no aswer for the question in the documents "
                    "tell about it straight and answer using your basic knowledge.\n\n"
                    f"KNOWLEDGE BASE DOCUMENTS:\n{full_context}"
                )

                messages_list.insert(0, {"role": "system", "content": system_prompt})

    result = send_query(messages_list)

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

        elif file.content_type.startswith(
            "application/vnd.openxmlformats-officedocument"
        ) or extension in [".docx", ".xlsx", ".pptx"]:
            result = md.convert_stream(binary_stream, file_extension=extension)
            text_content = result.text_content

        elif file.content_type.startswith("text/") or extension in [
            ".md",
            ".txt",
            ".html",
            ".csv",
            ".json",
        ]:
            text_content = file_bytes.decode()

        else:
            raise ValueError(f"Unsupported file extension: {extension}")

    except ValueError:
        raise HTTPException(status_code=400, detail="Wrong file type")
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {e!s}")

    if not text_content or text_content.strip() == "":
        raise HTTPException(
            status_code=400, detail="Empty file or no readable text found"
        )

    file_uuid = add_to_collection(text_content, file.filename)

    return {"filename": file.filename, "file_uuid": file_uuid}


@app.delete("/delete_file/{file_uuid}")
async def delete_file(file_uuid: str):
    is_deleted = delete_document(file_uuid)

    if not is_deleted:
        raise HTTPException(
            status_code=404, detail=f"File with UUID {file_uuid} was not found"
        )

    return {"message": "File deleted successfully", "file_uuid": file_uuid}
