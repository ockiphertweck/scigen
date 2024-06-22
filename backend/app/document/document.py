import os
from typing import List
from app.services.nougat import parsePdfToMardown, ping
from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import requests
from app.services.text_splitter import Splitter, SplitterOptions, split_text
from semanticscholar import SemanticScholar, PaginatedResults
from pydantic import BaseModel
from app.document.service.upload_service import DocumentUploadService


load_dotenv()
NOUGAT_URL = os.getenv('NOUGAT_URL', '')


class Document(BaseModel):
    title: str
    url: str


class SimilarDocumentResponse(BaseModel):
    message: str = Field(
        None, description="A message about the result of the operation")
    similar_docs: List[Document]


class DocumentResponse(BaseModel):
    message: str = Field(
        None, description="A message about the result of the operation")


router = APIRouter()
# async def uploadDocument(file: UploadFile = File(...), splitter: Splitter = Splitter.SEMANTIC_TEXT_SPLITTER_MD, chunk_size: int = 2000, chunk_overlap: int = 200, tokenizer_model_name: str = "gpt-4", schema_name: str = "PH_Document"):


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
async def upload_file(
    file: UploadFile = File(...),
    splitter: Splitter = Form(Splitter.SEMANTIC_TEXT_SPLITTER_MD),
    chunk_size: int = Form(2000),
    chunk_overlap: int = Form(200),
    tokenizer_model_name: str = Form("gpt-4"),
    schema_name: str = Form("PH_Documents")
):
    """
    Uploads a document, converts it to markdown, vectorizes it, and stores it in the database.

    Args:
        data (DocumentUploadService.DocumentUploadModel): The data required for document upload.

    Returns:
        A JSON response with status code 200 and a message indicating the successful conversion and storage of the document in the database.
    """
    try:
        data = DocumentUploadService.DocumentUploadModel(
            file=file,
            splitter=splitter,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            tokenizer_model_name=tokenizer_model_name,
            schema_name=schema_name
        )
        upload_service = DocumentUploadService()
        result = await upload_service.perform_action(data)
        return {"result": "result"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        raise HTTPException(
            status_code=503, detail="Nougat service is not available")


@router.get("/document/search",
            summary="Find similar papers using Semantic Scholar API",
            description="Retrieves a list of similar documents based on the given base document name. This is useful for finding relevant academic papers using Semantic Scholar's data.",
            response_model=SimilarDocumentResponse,
            responses={
                200: {"model": SimilarDocumentResponse, "description": "A list of similar documents is returned."},
                401: {"description": "API key is missing or invalid"},
                503: {"description": "Nougat service is not available"},
            },
            status_code=status.HTTP_200_OK,
            tags=["Document Processing"])
async def get_similar_documents(base_document_name: str, limit: int = 5):
    """
     Retrieves a list of similar documents based on the given base document name.

     Args:
         base_document_name (str): The name of the base document.
         limit (int, optional): The maximum number of similar documents to retrieve. Defaults to 5.

     Returns:
         A JSON response with status code 200 and a list of similar documents.

     Raises:
         HTTPException: If the API key is missing or invalid, returns a 401 Unauthorized status code.
    """
    dotEnv = find_dotenv()
    env = load_dotenv(dotenv_path=dotEnv)
    semantic_scolar_api_key = os.getenv('SEMANTIC_SCOLAR_API_KEY')
    sem_scholar: SemanticScholar
    if semantic_scolar_api_key is None or semantic_scolar_api_key == "":
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "API key is missing or invalid"})
    sem_scholar = SemanticScholar(api_key=semantic_scolar_api_key)
    similar_documents: PaginatedResults = sem_scholar.search_paper(
        query=base_document_name, open_access_pdf=True, limit=limit)
    documents = []
    for index, item in enumerate(similar_documents.items):
        document = {
            "title": item.title,
            "url": item.openAccessPdf
        }
        documents.append(document)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"documents": documents})
