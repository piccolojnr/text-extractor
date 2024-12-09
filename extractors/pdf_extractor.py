from PyPDF2 import PdfReader
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        text = ""
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")


def extract_text_and_images_from_pdf(file_path):
    """Extract text and images with OCR from a PDF."""
    text = ""
    try:
        # Open the PDF file
        pdf_document = fitz.open(file_path)

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]

            # Extract text from the page
            text += f"Page {page_number + 1}:\n"
            text += page.get_text("text") + "\n"

            # Extract images from the page
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))

                # Perform OCR on the image
                ocr_text = pytesseract.image_to_string(image)
                text += f"\nOCR from Image {img_index + 1} on Page {page_number + 1}:\n{ocr_text}\n"

        pdf_document.close()
    except Exception as e:
        raise RuntimeError(f"Failed to extract text and images from PDF: {e}")
    return text
