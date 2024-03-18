from typing import Dict
from fastapi import UploadFile
import requests

async def parsePdfToMardown(file: UploadFile, NOUGAT_URL: str):
   # Read file content
   file_content = await file.read()
   headers = {
       "Accept": "application/json",
   }
   response = await requests.post(NOUGAT_URL + "/predict", files={"file": file_content}, headers=headers)
   print(response.json())

   return response.json()

async def ping(NOUGAT_URL: str):
   response = await requests.get(NOUGAT_URL)
   return response