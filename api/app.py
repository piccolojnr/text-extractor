from fastapi import FastAPI
from api.routes import router

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Text Extraction API",
    description="A REST API for extracting text from various document formats.",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:5000",
]

# Allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes
app.include_router(router)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Text Extraction API"}
