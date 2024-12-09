import win32com.client


def extract_text_from_doc(file_path):
    """Extract text from a .doc file using pywin32."""
    try:
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(file_path)
        text = doc.Content.Text
        doc.Close()
        word.Quit()
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from DOC: {e}")
