from enum import Enum
import os
import requests


class Splitter(str, Enum):
    """Enum of available text splitters"""
    RECURSIVE_CHARACTER_MARKDOWN = "recursive_character_markdown"
    SEMANTIC_TEXT_SPLITTER = "semantic_text_splitter"
    SEMANTIC_TEXT_SPLITTER_MD = "semantic_text_splitter_md"
    SEMANTIC_SPLIT = "semantic_split"


def upload_document(file_path, url):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'splitter': Splitter.SEMANTIC_TEXT_SPLITTER_MD.value,
            'chunk_size': 3000,
            'chunk_overlap': 200,
            'tokenizer_model_name': 'gpt-4',
            'schema_name': 'PH_CEURWS'
        }
        print(files)
        print(data)
        response = requests.post(url, files=files, data=data)
        return response


def iterate_and_upload(base_folder):
    url = "http://localhost:8504/document/"
    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            if dir_name.startswith("Vol-"):
                vol_dir = os.path.join(root, dir_name)
                for file_name in os.listdir(vol_dir):
                    if file_name.endswith(".pdf"):
                        file_path = os.path.join(vol_dir, file_name)
                        print(f"Uploading {file_path}...")
                        response = upload_document(file_path, url)
                        print(
                            f"Response: {response.status_code} - {response.text}")


if __name__ == "__main__":
    base_folder = input("Enter the path to the base folder: ")
    iterate_and_upload(base_folder)
