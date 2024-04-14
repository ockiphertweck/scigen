import os
from typing import Dict
from app.services.nougat import parsePdfToMardown, ping
from fastapi import FastAPI
from app.document.document import router as document_router
from fastapi.responses import RedirectResponse
from langserve import add_routes
import uvicorn
from dotenv import load_dotenv, find_dotenv


app = FastAPI(
    title="SciGen",
    description="API documentation for the endpoints of the SciGen service",
    version="1.0.0"
)

app.include_router(document_router)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


def check_env_vars_set():
    """
    Check if the required environment variables are set.

    This function checks if the required environment variables are set. If any of the required environment variables
    are missing, it raises an exception with the name of the missing variable.

    :raises Exception: If any of the required environment variables are missing.
    """
    required_env_vars = ["WEAVIATE_HOST", "WEAVIATE_PORT",
                         "WEAVIATE_GRPC_PORT", "WEAVIATE_API_KEY", "NOUGAT_URL", "OPENAI_API_KEY"]
    for env_var in required_env_vars:
        if not os.getenv(env_var):
            raise Exception(
                f"Missing required environment variable: {env_var}")


def main():
    print("Server is starting...")
    load_dotenv(find_dotenv())

    check_env_vars_set()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    # Load environment variables from .env file
    main()
