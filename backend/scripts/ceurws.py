from enum import Enum
import os
import requests
import time


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
        response = requests.post(url, files=files, data=data)
        return response


def count_files(base_folder):
    total_files = 0
    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            if dir_name.startswith("Vol-"):
                vol_dir = os.path.join(root, dir_name)
                total_files += len([file for file in os.listdir(vol_dir)
                                   if file.endswith(".pdf")])
    return total_files


def iterate_and_upload(base_folder):
    url = "http://localhost:8504/document/"
    total_files = count_files(base_folder)
    current_index = 1

    start_time = time.time()

    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            if dir_name.startswith("Vol-"):
                vol_dir = os.path.join(root, dir_name)
                for file_name in os.listdir(vol_dir):
                    if file_name.endswith(".pdf"):
                        file_path = os.path.join(vol_dir, file_name)

                        file_start_time = time.time()
                        print(
                            f"[{current_index}/{total_files}]: Uploading {file_path}...")
                        response = upload_document(file_path, url)
                        file_end_time = time.time()

                        print(
                            f"Response: {response.status_code} - {response.text}")
                        print(
                            f"Time taken to upload {file_name}: {file_end_time - file_start_time:.2f} seconds")

                        current_index += 1

    end_time = time.time()
    total_processing_time = end_time - start_time
    print(f"Total processing time: {total_processing_time:.2f} seconds")


if __name__ == "__main__":
    base_folder = input("Enter the path to the base folder: ")
    iterate_and_upload(base_folder)
