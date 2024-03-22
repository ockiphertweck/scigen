from enum import Enum
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language


class Splitter(str, Enum):
    """Enum of available text splitters"""
    RECURSIVE_CHARACTER_MARKDOWN = "recursive_character_markdowb"
    SEMANTIC = "semantic"


def split_text(text: str, chunk_size: int, chunk_overlap: int,  splitter: Splitter) -> List[str]:
    """
    Splits the given text into chunks based on the specified splitter.

    Args:
        text (str): The text to be split.
        chunk_size (int): The desired size of each chunk.
        chunk_overlap (int): The amount of overlap between consecutive chunks.
        splitter (Splitter): The splitter option to be used for splitting the text.

    Returns:
        List[str]: A list of chunks obtained after splitting the text.

    Raises:
        ValueError: If an invalid splitter option is provided.
    """
    chunks: List[str] = []
    if splitter == Splitter.RECURSIVE_CHARACTER_MARKDOWN:
        chunks =  _recursive_character_markdown(text, chunk_size, chunk_overlap)
    elif splitter == Splitter.SEMANTIC:
        raise NotImplementedError("Semantic splitter is not implemented yet")
        pass
    else:
        raise ValueError("Invalid splitter option")
    return chunks





def _recursive_character_markdown(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """
    Splits the given text into chunks using the RecursiveCharacterTextSplitter with the Markdown language.

    Args:
        text (str): The text to be split into chunks.
        chunk_size (int): The desired size of each chunk.
        chunk_overlap (int): The amount of overlap between consecutive chunks.

    Returns:
        List[str]: A list of chunks obtained after splitting the text.
    """
    splitter = RecursiveCharacterTextSplitter(Language.MARKDOWN,chunk_size, chunk_overlap)
    chunks = splitter.split_text(text)
    return chunks