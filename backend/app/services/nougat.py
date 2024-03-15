from typing import Dict
from fastapi import UploadFile
import requests

async def convert_file_to_markdown(file: UploadFile, options: Dict[str, str]):
   # Read file content
   file_content = await file.read()
   headers = {
       "Accept": "application/json",
   }
   response = requests.post(options["NOUGAT_URL"] + "/predict", files={"file": file_content}, headers=headers)
   print(response.json())

   return response.json()
