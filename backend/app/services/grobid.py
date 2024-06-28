from typing import Dict
from fastapi import UploadFile
from requests import Response, post, get


async def parsePdfToXml(file: UploadFile, GROBID_URL: str) -> str:
    """
    Parses a PDF file to XML using the Grobid service.

    Args:
       file (UploadFile): The PDF file to be parsed.
       GROBID_URL (str): The URL of the Grobid service.

    Returns:
       dict: The parsed XML content as a string.

    Raises:
       Exception: If there is an error while parsing the PDF file.
    """
    file_content = await file.read()
    headers = {
        "Accept": "application/xml",
    }
    response: Response = post(GROBID_URL + "/api/processFulltextDocument",
                              files={"input": file_content},
                              data={"teiCoordinates": ["figure", "table"]},
                              headers=headers)
    response.raise_for_status()
    if not response.ok:
        raise Exception("Error parsing PDF to XML")
    return response.text


async def ping(GROBID_URL: str):
    """
    Sends a ping request to the specified GROBID_URL and returns the response.

    Args:
       GROBID_URL (str): The URL to send the ping request to.

    Returns:
       The response from the ping request.
    """
    response = await get(GROBID_URL)
    return response
