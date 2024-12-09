def extract_text_from_txt(file_path):
    """Extract text from a TXT."""
    text = ""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
    except Exception as e:
        print(f"Error reading TXT: {e}")
    return text
