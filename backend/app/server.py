from typing import Dict
from app.services.nougat import parsePdfToMardown, ping
from fastapi import FastAPI
from app.document.document import router as  document_router
from fastapi.responses import RedirectResponse
from langserve import add_routes


app = FastAPI(
    title="SciGen",
    description="API documentation for the endpoints of the SciGen service",
    version="1.0.0"
)

app.include_router(document_router)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")




# Edit this to add the chain you want to add
#add_routes(app, NotImplemented)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
