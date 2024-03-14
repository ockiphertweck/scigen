from fastapi import File

def convert_file_to_markdown(file: File):
   print(file)
   return {"message": f"Success uploaded {file.filename}"}