from fastapi import FastAPI

from src.routers import documents

app = FastAPI(title="File Assistant")

app.include_router(documents.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
