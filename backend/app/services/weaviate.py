from pydantic import BaseModel
from typing import Optional
import threading
from weaviate.auth import AuthCredentials
import weaviate
import os
from dotenv import load_dotenv


class WeaviateConfig(BaseModel):
    """
    Configuration class for Weaviate service.

    Attributes:
        auth_credentials (AuthCredentials): The authentication credentials for Weaviate.
        http_host (str): The HTTP host of the Weaviate service.
        grpc_host (str): The gRPC host of the Weaviate service.
        http_port (int): The HTTP port of the Weaviate service.
        grpc_port (int): The gRPC port of the Weaviate service.
        http_secure (bool): Flag indicating whether the HTTP connection should be secure.
        grpc_secure (bool): Flag indicating whether the gRPC connection should be secure.
    """
    auth_credentials: AuthCredentials
    http_host: str
    grpc_host: str
    http_port: int
    grpc_port: int
    http_secure: bool
    grpc_secure: bool


class WeaviateClient:
    """
    A singleton client class for interacting with the Weaviate service.

    This class provides a singleton instance of the Weaviate client, ensuring that only one instance
    is created and used throughout the application.

    Args:
        config (WeaviateConfig): The configuration object containing the Weaviate connection details.

    Attributes:
        client: The Weaviate client instance.

    """

    _instance: Optional["WeaviateClient"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        load_dotenv()
        config = WeaviateConfig(
            auth_credentials=weaviate.auth.Auth.api_key(
                os.getenv('WEAVIATE_API_KEY', "")),
            http_host=os.getenv('WEAVIATE_HOST', 'localhost'),
            grpc_host=os.getenv('WEAVIATE_HOST_GRPC', 'localhost'),
            http_port=int(os.environ.get('WEAVIATE_PORT', '443')),
            grpc_port=int(os.environ.get('WEAVIATE_GRPC_PORT', '443')),
            http_secure=True,
            grpc_secure=True,
        )
        self.client = weaviate.connect_to_custom(
            auth_credentials=config.auth_credentials,
            http_host=config.http_host,
            grpc_host=config.grpc_host,
            http_port=config.http_port,
            grpc_port=config.grpc_port,
            http_secure=config.http_secure,
            grpc_secure=config.grpc_secure,
        )


@staticmethod
def create_vector_store(client, embeddings, index_name: str, text_key: str):
    """
    Create a WeaviateVectorStore object.

    Args:
        client: The Weaviate client object.
        embeddings: The embeddings to be used for vectorization.
        index_name: The name of the index in Weaviate.
        text_key: The key in the Weaviate objects that contains the text data.

    Returns:
        A WeaviateVectorStore object.

    """
    from langchain_weaviate.vectorstores import WeaviateVectorStore
    return WeaviateVectorStore(client=client, embedding=embeddings, index_name=index_name, text_key=text_key)
