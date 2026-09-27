from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="LegalEase - AI Legal Document Generator",
    version="1.0.0",
    description="FastAPI backend for AI-assisted legal document drafting.",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Welcome to LegalEase AI Legal Document Generator API",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("legalEaseAPI.main:app", host="0.0.0.0", port=8000, reload=True)
