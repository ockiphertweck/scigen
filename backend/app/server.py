from typing import Dict
from app.services.nougat import convert_file_to_markdown
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from fastapi import File, UploadFile
import os
from dotenv import load_dotenv

load_dotenv()
NOUGAT_URL = os.getenv('NOUGAT_URL')
options: Dict[str, str] = {
    "NOUGAT_URL": NOUGAT_URL
}
app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    response = await convert_file_to_markdown(file, options)
    return response


# Edit this to add the chain you want to add
#add_routes(app, NotImplemented)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
