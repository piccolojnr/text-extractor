

# **Text Extraction Tool**

## **Overview**
The Text Extraction Tool is a robust Python application designed to extract text from various document formats. It supports plain text extraction, embedded image OCR (Optical Character Recognition), and batch processing of files. This tool is optimized for extensibility, allowing support for additional formats and features.

---

## **Features**
1. **Supported File Types**:
   - PDF: Extracts text from pages and performs OCR on embedded images.
   - PPTX: Extracts text from slides and performs OCR on embedded images.
   - DOCX: Extracts text from Word documents and performs OCR on embedded images.
   - Images (PNG, JPG, JPEG): Extracts text using OCR.
   - TXT: Reads plain text files.

2. **Batch Processing**:
   - Processes all supported files in a specified directory.
   - Option to save extracted text to a specified output directory.

3. **Concurrency**:
   - Uses multi-threading for faster processing of multiple files and OCR tasks.

4. **OCR (Optional)**:
   - Extracts text from images within documents using Tesseract OCR.
   - Can be enabled or disabled using the `--enable-ocr` flag.

5. **Error Handling**:
   - Logs errors for unsupported files or processing issues without interrupting the workflow.

6. **Modularity**:
   - Designed with a modular architecture for easy maintenance and scalability.

---

## **Installation**

### **Dependencies**
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

Install Tesseract OCR:
- **Linux**:
  ```bash
  sudo apt install tesseract-ocr
  ```
- **macOS**:
  ```bash
  brew install tesseract
  ```
- **Windows**:
  Download and install from [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).

### **Required Python Libraries**
Include the following in your `requirements.txt`:
```plaintext
PyMuPDF
python-pptx
python-docx
Pillow
pytesseract
```

---

## **Usage**

### **Extract Text from a Single File**
```bash
python main.py sample.pdf
```

### **Extract Text and Save to File**
```bash
python main.py sample.pdf -o output/
```

### **Enable OCR for Embedded Images**
```bash
python main.py sample.pdf --enable-ocr
```

### **Batch Process a Directory**
Extract text from all supported files in a directory:
```bash
python main.py documents/ -o extracted/
```

### **Batch Processing with OCR**
Enable OCR for images in all supported files:
```bash
python main.py documents/ -o extracted/ --enable-ocr
```

### **Specify the Number of Workers for Parallel Processing**
```bash
python main.py documents/ -o extracted/ --enable-ocr -w 8
```

---

## **File Structure**
```
text_extractor/
├── main.py                # Entry point of the application
├── extractors/            # Module for text extractors
│   ├── __init__.py        # Package initializer
│   ├── pdf_extractor.py   # PDF extraction logic (text and OCR)
│   ├── pptx_extractor.py  # PPTX extraction logic (text and OCR)
│   ├── docx_extractor.py  # DOCX extraction logic (text and OCR)
│   ├── txt_extractor.py   # TXT file extraction logic
│   ├── image_extractor.py # Image OCR logic
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── file_utils.py      # File validation and utility functions
│   ├── logger.py          # Logging utility
├── requirements.txt       # List of dependencies
└── README.md              # Project documentation
```

---

## **Key Components**

### **Main Application (`main.py`)**
- Handles command-line arguments and directs files to the appropriate extractor.
- Supports single-file and batch processing.
- Optional concurrency for faster processing.

### **Extractors**
- **PDF Extractor**: Handles text and image extraction from PDF files.
- **PPTX Extractor**: Extracts text and OCR from PowerPoint slides.
- **DOCX Extractor**: Extracts text and OCR from Word documents.
- **Image Extractor**: Performs OCR on standalone image files.
- **TXT Extractor**: Reads plain text files.

### **Utilities**
- **File Utilities**: Handles file validation and type detection.
- **Logger**: Centralized logging for errors and progress tracking.

---

## **Future Improvements**
1. **Additional File Types**:
   - Add support for `.xlsx` (Excel) and `.html` (HTML files).
   - Include `.zip` archives for processing compressed files.

2. **OCR Optimization**:
   - Use GPU-accelerated OCR tools like EasyOCR for faster processing.
   - Implement selective OCR (only process images if text is not detected).

3. **Progress Tracking**:
   - Display a progress bar for batch processing (e.g., using `tqdm`).

4. **Error Reporting**:
   - Generate detailed logs and summary reports for failed files.

5. **Customizable Output**:
   - Allow users to specify output format (e.g., plain text, JSON).

6. **Web Interface**:
   - Develop a Flask or FastAPI-based web interface for user-friendly interaction.

7. **Cloud Integration**:
   - Integrate with cloud OCR APIs like Google Vision or AWS Textract for more accurate text extraction.

8. **Testing and CI/CD**:
   - Add automated tests for extractors.
   - Implement continuous integration for robust development workflows.

---

## **Contributing**
Contributions are welcome! If you’d like to add new features or fix bugs, please fork the repository, make your changes, and submit a pull request.

---

## **License**
This project is licensed under the MIT License.

---
