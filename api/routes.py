import json
from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pathlib import Path
from api.start import (
    SUPPORTED_EXTENSIONS,
    extract_text as extract_text_from_file,
    extract_text_from_files,
)
from utils.create_ppts import create_pptx_from_flashcards, styles
from utils.file_utils import get_file_extension
from io import BytesIO

router = APIRouter()


# supported file types
@router.get("/supported-file-types")
async def supported_file_types():
    """
    Get a list of supported file types.
    """
    return {"supported_file_types": SUPPORTED_EXTENSIONS}


# extract text from file
@router.post("/extract")
async def extract_text(file: UploadFile = File(...), enable_ocr: bool = Form(False)):
    """
    Extract text from an uploaded file.
    """
    try:
        # Validate file extension
        file_extension = get_file_extension(file.filename)
        if file_extension not in SUPPORTED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Save the uploaded file temporarily
        temp_file_path = Path(f"temp/{file.filename}")
        temp_file_path.parent.mkdir(exist_ok=True)
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Extract text
        result = extract_text_from_file(temp_file_path, enable_ocr)

        # Clean up temporary file
        temp_file_path.unlink()

        if result[1] == 200:
            extracted_text = result[0]
            return {"filename": file.filename, "extracted_text": extracted_text}
        else:
            raise HTTPException(status_code=result[1], detail=result[0])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# extract text from multiple files
@router.post("/extract-batch")
async def extract_text_batch(
    files: list[UploadFile] = File(...),
    enable_ocr: bool = Form(False),
    max_workers: int = Form(None),
):
    """
    Extract text from multiple uploaded files concurrently.
    """
    try:
        # Save uploaded files temporarily
        temp_files = []
        for file in files:
            temp_file_path = Path(f"temp/{file.filename}")
            temp_file_path.parent.mkdir(exist_ok=True)
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(await file.read())
            temp_files.append(temp_file_path)

        # Process files
        results, status_code = extract_text_from_files(
            temp_files, enable_ocr, max_workers
        )

        # Clean up temporary files
        for temp_file in temp_files:
            temp_file.unlink()

        return {"results": results}, status_code
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-pptx/")
async def generate_pptx(request: Request):

    # Parse the request body as JSON
    body = await request.json()
    flashcards = body.get("flashcards", [])
    style = body.get("style", "classic")

    # # Create the PowerPoint presentation
    presentation = create_pptx_from_flashcards(flashcards, style)

    # # Save the presentation to a BytesIO stream
    pptx_stream = BytesIO()
    presentation.save(pptx_stream)
    pptx_stream.seek(0)

    # Return the PPTX file as a response
    return StreamingResponse(
        pptx_stream,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": "attachment; filename=flashcards.pptx"},
    )


@router.get("/styles/")
async def get_styles():
    """
    Get a list of supported styles for creating flashcards.
    """
    return {"styles": list(styles.keys())}
