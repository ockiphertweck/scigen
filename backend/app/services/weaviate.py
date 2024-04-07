

from typing import List
from langchain_core.documents import Document
from langchain_weaviate.vectorstores import WeaviateVectorStore
import weaviate
import os
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_core.embeddings.embeddings import Embeddings


def store_documents(documents: List[Document], embeddings: Embeddings = OpenAIEmbeddings(), collection_name: str = "wiki_docs"):
    """
    Store the given list of documents in the Weaviate database.

    Args:
        documents (List[Document]): A list of Document objects to be stored in the database.
        embeddings (Embeddings, optional): An instance of the Embeddings class to be used for generating document embeddings. Defaults to OpenAIEmbeddings().
        collection_name (str, optional): The name of the collection in the Weaviate database where the documents will be stored. Defaults to "wiki_docs".

    Returns:
        None
    """
    weaviate_client = WeaviateClient.get_instance()
    weaviate = WeaviateVectorStore(
        client=weaviate_client, index_name=collection_name, embedding=embeddings)
    weaviate.add_documents(documents)


class WeaviateClient:
    """
    A singleton client class for interacting with the Weaviate service.

    This class provides a singleton instance of the Weaviate client, ensuring that only one instance
    is created throughout the application.

    Usage:
        client = WeaviateClient.get_instance()
    """

    _instance = None

    @ staticmethod
    def get_instance():
        """
        Get the singleton instance of the Weaviate client.

        Returns:
            WeaviateClient: The singleton instance of the Weaviate client.
        """
        if WeaviateClient._instance is None:
            WeaviateClient()
        return WeaviateClient._instance

    def __init__(self):
        """
        Initialize the Weaviate client.

        Raises:
            Exception: If a singleton instance already exists.
        """
        if WeaviateClient._instance is not None:
            raise Exception(
                "Singleton instance already exists. Use get_instance() method to access it.")
        else:
            # Create a singleton instance of the Weaviate client
            WeaviateClient._instance = weaviate.connect_to_custom(
                http_host=os.getenv("WEAVIATE_HOST"),
                http_port=os.getenv("WEAVIATE_PORT"),
                http_secure=True,
                grpc_host=os.getenv("WEAVIATE_HOST"),
                grpc_port=os.getenv("WEAVIATE_GRPC_PORT"),
                grpc_secure=True,
                auth_credentials=weaviate.auth.AuthApiKey(
                    os.getenv("WEAVIATE_API_KEY"))
            )
