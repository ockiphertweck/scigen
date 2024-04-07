import os

from services.nougat import parsePdfToMardown
from services.text_splitter import SplitterOptions, split_text

folder_path = os.getenv("FOLDER_PATH")
NOUGAT_URL = os.getenv('NOUGAT_URL')
splitter = os.getenv("SPLITTER")
chunk_size = os.getenv("CHUNK_SIZE")
tokenizer_model_name = os.getenv("TOKENIZER_MODEL_NAME")
from fastapi import UploadFile


async def uploadDocument(file_path):
    print(f"Uploading document: {file_path}")
    with open(file_path, "rb") as file:
        upload_file = UploadFile(file, filename=file_path)
        markdown_content = await parsePdfToMardown(upload_file, NOUGAT_URL)
        chunks = split_text(markdown_content, splitter, splitter_options=SplitterOptions(chunk_size=chunk_size, chunk_overlap=0, tokenizer_model_name=tokenizer_model_name))
    

def process_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            uploadDocument(file_path)

if __name__ == "__main__":
    if folder_path:
        process_files(folder_path)
    else:
        print("Please set the FOLDER_PATH environment variable.")