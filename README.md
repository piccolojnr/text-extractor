
# **Text Extraction Tool**

## **Overview**
The Text Extraction Tool is a robust Python application designed to extract text from various document formats. It supports plain text extraction, embedded image OCR (Optical Character Recognition), batch processing of files, and concurrent processing for improved performance. This tool is optimized for extensibility, allowing support for additional formats and features.

---

## **Features**
1. **Supported File Types**:
   - PDF: Extracts text from pages and performs OCR on embedded images.
   - PPTX: Extracts text from slides and performs OCR on embedded images.
   - DOCX: Extracts text from Word documents and performs OCR on embedded images.
   - Images (PNG, JPG, JPEG): Extracts text using OCR.
   - TXT: Reads plain text files.

2. **Batch Processing**:
   - Processes multiple files in a single API request or directory scan.
   - Skips unsupported file types and logs warnings.

3. **Concurrency**:
   - Leverages multi-threading to process files in parallel, significantly improving performance for large workloads.

4. **OCR (Optional)**:
   - Extracts text from images within documents using Tesseract OCR.
   - Can be enabled or disabled using the `--enable-ocr` flag.

5. **REST API**:
   - Offers a FastAPI-based web interface for file uploads and text extraction.

6. **Error Handling**:
   - Logs errors for unsupported files or processing issues without interrupting the workflow.
   - Returns detailed error responses for failed files.

7. **Modularity**:
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
fastapi
uvicorn
PyMuPDF
python-pptx
python-docx
Pillow
pytesseract
tqdm
```

---

## **Usage**

### **1. CLI Usage**

#### **Extract Text from a Single File**
```bash
python main.py sample.pdf
```

#### **Extract Text and Save to File**
```bash
python main.py sample.pdf -o output/
```

#### **Enable OCR for Embedded Images**
```bash
python main.py sample.pdf --enable-ocr
```

#### **Batch Process a Directory**
Extract text from all supported files in a directory:
```bash
python main.py documents/ -o extracted/
```

#### **Batch Processing with OCR**
Enable OCR for images in all supported files:
```bash
python main.py documents/ -o extracted/ --enable-ocr
```

#### **Specify the Number of Workers for Concurrent Processing**
```bash
python main.py documents/ -o extracted/ --enable-ocr -w 8
```

---

### **2. API Usage**

#### **Run the FastAPI Server**
Start the server using `uvicorn`:
```bash
uvicorn api.app:app --reload
```

#### **API Endpoints**
1. **Extract Text from a Single File**
   - **Endpoint**: `/extract`
   - **Method**: `POST`
   - **Parameters**:
     - `file`: The file to be uploaded.
     - `enable_ocr`: Boolean to enable OCR for embedded images.
   - **Response**:
     - `filename`: The name of the processed file.
     - `extracted_text`: The extracted text.

2. **Batch Extract Text**
   - **Endpoint**: `/extract_batch`
   - **Method**: `POST`
   - **Parameters**:
     - `files`: A list of files to be uploaded.
     - `enable_ocr`: Boolean to enable OCR for embedded images.
     - `max_workers`: Number of threads for concurrent processing (optional).
   - **Response**:
     - List of results, including filenames, extracted text, and status codes.

#### **Example API Request (Batch)**
```bash
curl -X POST "http://127.0.0.1:8000/extract_batch" \
-H "accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "files=@file1.pdf" \
-F "files=@file2.pptx" \
-F "enable_ocr=true" \
-F "max_workers=4"
```

---

## **File Structure**
```
text_extractor/
├── main.py                # CLI entry point
├── api/                   # API module
│   ├── __init__.py        # Package initializer
│   ├── app.py             # FastAPI app definition
│   ├── routes.py          # API routes
├── extractors/            # Extraction logic
│   ├── __init__.py
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
└── README.md              # Documentation
```

---

## **Features Added**
1. **Batch Processing**:
   - Allows multiple files to be processed in a single request or command.
   - Concurrently processes files using multi-threading.

2. **Concurrency**:
   - Speeds up processing for large workloads using `ThreadPoolExecutor`.

3. **REST API**:
   - Provides endpoints for single-file and batch extraction.
   - Offers concurrency control via the `max_workers` parameter.

---

## **Future Improvements**
1. **Additional File Types**:
   - Add support for `.xlsx` (Excel) and `.html` (HTML files).
   - Handle `.zip` archives for batch processing of compressed files.

2. **Asynchronous Processing**:
   - Switch to `asyncio` for handling I/O-bound tasks efficiently.

3. **Progress Tracking**:
   - Add real-time progress tracking for API requests and batch CLI operations.

4. **Frontend Integration**:
   - Develop a React or Vue.js interface for user-friendly uploads and results display.

5. **Cloud Deployment**:
   - Deploy the API to a cloud environment (AWS, Azure, Heroku) with auto-scaling capabilities.

6. **Database Integration**:
   - Store extracted text and metadata in a database for search and analytics.

7. **Authentication**:
   - Add user authentication for secure API usage.

---

## **Contributing**
Contributions are welcome! If you’d like to add new features or fix bugs, please fork the repository, make your changes, and submit a pull request.

---

## **License**
This project is licensed under the MIT License.

