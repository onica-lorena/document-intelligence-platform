from fastapi import FastAPI

app = FastAPI(
    title="Document Intelligence Platform API",
    description="Backend API for document ingestion, processing and question answering.",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": "Document Intelligence Platform API is running!"
    }