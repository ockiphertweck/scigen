import os
from app.common.base_service import BaseService
from app.services.nougat import parsePdfToMardown
from app.services.text_splitter import Splitter, SplitterOptions, split_text
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import File, HTTPException, UploadFile, status
from dotenv import load_dotenv


class DocumentUploadService(BaseService):
    class DocumentUploadModel(BaseModel):
        file: UploadFile
        splitter: Splitter
        chunk_size: int
        chunk_overlap: int
        tokenizer_model_name: str
        schema_name: str

    async def perform_action(self, data: DocumentUploadModel):
        from app.services.weaviate import WeaviateClient, create_vector_store
        from langchain_openai import OpenAIEmbeddings
        load_dotenv()
        try:
            print(data)
            markdown_content = await parsePdfToMardown(data.file, NOUGAT_URL=os.getenv("NOUGAT_URL", ""))
            documents, references = split_text(markdown_content, data.splitter, splitter_options=SplitterOptions(
                chunk_size=data.chunk_size, chunk_overlap=data.chunk_overlap, tokenizer_model_name=data.tokenizer_model_name), meta_data={"file_name": data.file.filename})
            weaviate_singleton = WeaviateClient()
            weaviate_client = weaviate_singleton.client
            embeddings = OpenAIEmbeddings()
            vectore_store = create_vector_store(
                weaviate_client, embeddings=embeddings, index_name=data.schema_name, text_key="text")
            vectore_store.add_documents(documents)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Conversion successful and document stored in the database"})
        except Exception as e:
            error_message = str(e)
            print(error_message)
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": error_message})
