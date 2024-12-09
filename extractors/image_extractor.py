from PIL import Image
import pytesseract


def extract_text_from_image(file_path):
    """Extract text from an image using OCR."""
    try:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from image: {e}")
