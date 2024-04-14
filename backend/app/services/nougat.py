from typing import Dict
from fastapi import UploadFile
from requests import Response, post, get


async def parsePdfToMardown(file: UploadFile, NOUGAT_URL: str) -> str:
    """
    Parses a PDF file to Markdown using the NOUGAT service.

    Args:
       file (UploadFile): The PDF file to be parsed.
       NOUGAT_URL (str): The URL of the NOUGAT service.

    Returns:
       dict: The parsed Markdown content as a string.

    Raises:
       Exception: If there is an error while parsing the PDF file.
    """
    file_content = await file.read()
    headers = {
        "Accept": "application/json",
    }
    response: Response = post(NOUGAT_URL + "/predict",
                              files={"file": file_content}, headers=headers)
    response.raise_for_status()
    if not response.ok:
        raise Exception("Error parsing PDF to Markdown")
    return response.json()


async def ping(NOUGAT_URL: str):
    """
    Sends a ping request to the specified NOUGAT_URL and returns the response.

    Args:
       NOUGAT_URL (str): The URL to send the ping request to.

    Returns:
       The response from the ping request.
    """
    response = await get(NOUGAT_URL)
    return response
