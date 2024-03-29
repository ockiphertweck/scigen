import os
from services.nougat import parsePdfToMardown, ping
from dotenv import load_dotenv
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import requests
from services.text_splitter import Splitter, split_text


load_dotenv()
NOUGAT_URL = os.getenv('NOUGAT_URL')

class DocumentResponse(BaseModel):
    message: str = Field(None, description="A message about the result of the operation")


router = APIRouter()

@router.get("/document/")
async def getDocument():
    return {"document": ["document 1", "document 2"]}


@router.post("/document/", 
    summary="Upload, Convert, Vectorize, and Store Document",
    description="This endpoint allows for uploading a document file, converts it to markdown format, vectorizes the content, and stores it in the database.",
    response_model=DocumentResponse,
    responses={
        200: {"model": DocumentResponse, "description": "Successful conversion, vectorization, and storage"},
        400: {"description": "Invalid file format or processing error"},
    },
    status_code=status.HTTP_200_OK,
    tags=["Document Processing"])

async def uploadDocument(file: UploadFile = File(...)):
    """
    Uploads a document, converts it to markdown, vectorizes it and stores it in the database.  

    - **file**: A document file that you want to convert to markdown.
    """
    markdown_content = await parsePdfToMardown(file, NOUGAT_URL)
    print(markdown_content)
   # chunked_text = split_text(markdown_content, Splitter.RECURSIVE_CHARACTER_MARKDOWN)
    #print(chunked_text[0])
    #print(len(chunked_text))
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Conversion successful and document stored in the database", "markdown": markdown_content})


@router.get("/document/parser/ping", 
    summary="Ping Nougat Service",
    description="Pings the Nougat service to check its availability and responsiveness. This is useful for health checks and monitoring the status of the Nougat service.",
    response_model=DocumentResponse,
    responses={
        200: {"model": DocumentResponse, "description": "Nougat service is responsive"},
        503: {"description": "Nougat service is not available"},
    },
    status_code=status.HTTP_200_OK,
    tags=["Document Processing"])
async def ping_nougat():
    """
    Pings the Nougat service to check its availability.  

    This endpoint sends a request to the Nougat service to verify it is up and running. It is useful for automated health checks or for manual verification of the service status.
    """
    try:
        response = ping(NOUGAT_URL)
        return {"status": "success", "message": "Nougat service is up and responsive"}
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Nougat service is not available")




