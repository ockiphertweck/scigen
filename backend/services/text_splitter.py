from enum import Enum
import re
from typing import List, Tuple
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from semantic_text_splitter import TextSplitter, MarkdownSplitter
from semantic_split import SimilarSentenceSplitter, SentenceTransformersSimilarity, SpacySentenceSplitter



class Splitter(str, Enum):
    """Enum of available text splitters"""
    RECURSIVE_CHARACTER_MARKDOWN = "recursive_character_markdown"
    SEMANTIC_TEXT_SPLITTER = "semantic_text_splitter"
    SEMANTIC_TEXT_SPLITTER_MD = "semantic_text_splitter_md"
    SEMANTIC_SPLIT = "semantic_split"
    SELF_SEMANTIC_SPLITTER = "self_semantic_splitter"

class SplitterOptions:
    """Options for the text splitter"""
    def __init__(self, chunk_size: int=2000, chunk_overlap: int=200, tokenizer_model_name="gpt-4"):
        """
        Initialize the SplitterOptions class.

        Args:
            chunk_size (int, optional): The size of each text chunk. Defaults to 2000.
            chunk_overlap (int, optional): The overlap between consecutive text chunks. Defaults to 200.
            tokenizer_model_name (str, optional): The name of the tokenizer model to use. Defaults to "gpt-4".
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.tokenizer_model_name = tokenizer_model_name

def split_text(text: str, splitter: Splitter, splitter_options: SplitterOptions) -> Tuple[List[str], str]:
    """
    Splits the given text into chunks based on the specified splitter.

    Args:
        text (str): The text to be split.
        splitter (Splitter): The splitter option to be used for splitting the text.
        splitter_options (SplitterOptions): The options to be used with the splitter.

    Returns:
        Tuple[List[str], str]: A tuple containing a list of chunks obtained after splitting the text and the references.

    Raises:
        ValueError: If an invalid splitter option is provided.
    """
    data: str
    tables: List[str]
    references: str
    data, tables, references = _pre_process_data(text)
    chunks: List[str] = []
    if splitter == Splitter.RECURSIVE_CHARACTER_MARKDOWN:
        chunks =  _recursive_character_markdown(data, splitter_options)
    elif splitter == Splitter.SEMANTIC_TEXT_SPLITTER:
        chunks = _semantic_text_splitter(data, splitter_options)
    elif splitter == Splitter.SEMANTIC_TEXT_SPLITTER_MD:
        chunks = _semantic_text_splitter_md(data, splitter_options)
    elif splitter == Splitter.SEMANTIC_SPLIT:
        chunks = _semantic_split(data, splitter_options)
    else:
        raise ValueError("Invalid splitter option")
    chunks = tables + chunks
    return chunks, references


def _recursive_character_markdown(text: str, splitter_options: SplitterOptions) -> List[str]:
    """
    Splits the given text into chunks using the RecursiveCharacterTextSplitter with the Markdown language.

    Args:
        text (str): The text to be split into chunks.
        splitter_options (SplitterOptions): The options for the splitter, including chunk size and overlap.

    Returns:
        List[str]: A list of chunks obtained after splitting the text.
    """
    splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(separators=Language.MARKDOWN, chunk_size=splitter_options.chunk_size, chunk_overlap=splitter_options.chunk_overlap)
    chunks: List[str] = splitter.split_text(text)
    return chunks

def _semantic_text_splitter(text: str, splitter_options: SplitterOptions) -> List[str]:
    """
    Splits the given text into chunks using the semantic-texst-splitter package.

    Args:
        text (str): The text to be split into chunks.
        splitter_options (SplitterOptions): The options for the splitter.


    Returns:
        List[str]: A list of chunks obtained after splitting the text.
    """
    splitter: TextSplitter = TextSplitter.from_tiktoken_model(model=splitter_options.tokenizer_model_name)
    chunks: List[str] = splitter.chunks(text, chunk_capacity=splitter_options.chunk_size)
    return chunks

def _semantic_text_splitter_md(text: str, splitter_options: SplitterOptions) -> List[str]:
    """
    Splits the given text into chunks using the semantic-texst-splitter package with markdown language.

    Args:
        text (str): The text to be split into chunks.
        splitter_options (SplitterOptions): The options for the splitter.

    Returns:
        List[str]: A list of chunks obtained after splitting the text.
    """
    splitter: MarkdownSplitter = MarkdownSplitter.from_tiktoken_model(model=splitter_options.tokenizer_model_name)
    chunks: List[str] = splitter.chunks(text, chunk_capacity=splitter_options.chunk_size)
    return chunks

def _semantic_split(text: str, splitter_options: SplitterOptions) -> List[str]:
    """
    Splits the given text into chunks using the semantic-split package.

    Args:
        text (str): The text to be split into chunks.
        splitter_options (SplitterOptions): The options for the splitter.

    Returns:
        List[str]: A list of chunks obtained after splitting the text.
    """
    model: SentenceTransformersSimilarity = SentenceTransformersSimilarity()
    sentence_splitter: SpacySentenceSplitter = SpacySentenceSplitter()
    splitter: SimilarSentenceSplitter = SimilarSentenceSplitter(model, sentence_splitter)
    chunks: List[str] = splitter.split(text)
    return chunks

def _find_and_remove_patter(data: str, pattern: str) -> Tuple[str, List[str]]:
    """
    Finds and removes the specified pattern from the given data.

    Args:
        data (str): The input data.
        pattern (str): The pattern to be found and removed.

    Returns:
        Tuple[str, List[str]]: A tuple containing the modified data and a list of found patterns.
    """
    found_pattern: List[str] = re.findall(pattern, data, re.DOTALL)
    for entry in found_pattern:
        data = re.sub(re.escape(entry), '', data)
    return data, found_pattern

def _extract_tables(data: str) -> Tuple[str, List[str]]:
    """
    Extracts tables from the given data.

    Args:
        data (str): The input data containing tables.

    Returns:
        Tuple[str, List[str]]: A tuple containing the modified data and a list of extracted tables.
    """
    pattern_table: str = r"\\begin{table}.*?\\end{table}"
    pattern_tabulate: str = r"\\begin{tabular}.*?\\end{tabular}"

    data: str
    tables1: List[str]
    tables2: List[str]
    data, tables1 = _find_and_remove_patter(data, pattern_table)
    data, tables2 = _find_and_remove_patter(data, pattern_tabulate)

    tables: List[str] = tables1 + tables2
    return data, tables

def _extract_references(data: str) -> Tuple[str, str]:
    """
    Extracts references from the given data.

    Args:
        data (str): The input data containing references.

    Returns:
        Tuple[str, str]: A tuple containing the modified data and a extracted references.
    """
    search_array: List[str] = [ "## References", "# References","**References**"]
    for search_term in search_array:
        if data.find(search_term) != -1:
            data = data.split(search_term)
            return data[0], data[1]

def _pre_process_data(text: str) -> Tuple[str, List[str], str]:
    """
    Pre-processes the given text by extracting tables and references.

    Args:
        text (str): The input text.

    Returns:
        Tuple[str, List[str], str]: A tuple containing the pre-processed data, extracted tables, and extracted references.
    """
    data: str
    tables: List[str]
    references: List[str]
    data, tables = _extract_tables(text)
    data, references = _extract_references(text)

    return data, tables, references




