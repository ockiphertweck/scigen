import os
from app.services.nougat import parsePdfToMardown, ping
from dotenv import load_dotenv
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import requests


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
    response = await parsePdfToMardown(file, NOUGAT_URL)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Conversion successful and document stored in the database"})


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
    # Assuming `ping` is defined elsewhere and pings the NOUGAT_URL
    try:
        # Assuming `ping` is a synchronous function making a request to NOUGAT_URL
        # You may need to adjust this if `ping` is already an async function
        response = ping(NOUGAT_URL)
        # If the request was successful, return a success message
        return {"status": "success", "message": "Nougat service is up and responsive"}
    except requests.exceptions.ConnectionError:
        # If a connection error occurs, return a meaningful error response
        raise HTTPException(status_code=503, detail="Nougat service is not available")




