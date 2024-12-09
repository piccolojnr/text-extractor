from fastapi import FastAPI
from api.routes import router


app = FastAPI(
    title="Text Extraction API",
    description="A REST API for extracting text from various document formats.",
    version="1.0.0",
)


# Include the routes
app.include_router(router)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Text Extraction API"}
