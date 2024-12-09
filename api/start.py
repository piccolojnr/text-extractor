import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from extractors.pdf_extractor import (
    extract_text_from_pdf,
    extract_text_and_images_from_pdf,
)
from extractors.pptx_extractor import (
    extract_text_from_pptx,
    extract_text_and_images_from_pptx,
)
from extractors.image_extractor import extract_text_from_image
from extractors.docx_extractor import (
    extract_text_from_docx,
    extract_text_and_images_from_docx,
)
from extractors.txt_extractor import extract_text_from_txt
from utils.file_utils import get_file_extension, validate_file_exists
from utils.logger import setup_logger

logger = setup_logger()

SUPPORTED_EXTENSIONS = [
    ".pdf",
    ".pptx",
    ".png",
    ".jpg",
    ".jpeg",
    ".txt",
    ".docx",
    # '.doc', '.xls', '.xlsx', '.csv', '.json', '.xml', '.html', '.log'
]


def extract_text(file_path, enable_ocr=False) -> tuple[str, int]:
    """Main function to extract text based on file type."""
    file_extension = get_file_extension(file_path)

    try:
        if file_extension == ".pdf":
            return (
                extract_text_and_images_from_pdf(file_path)
                if enable_ocr
                else extract_text_from_pdf(file_path)
            ), 200
        elif file_extension == ".pptx":
            return (
                extract_text_and_images_from_pptx(file_path)
                if enable_ocr
                else extract_text_from_pptx(file_path)
            ), 200
        elif file_extension in [".png", ".jpg", ".jpeg"]:
            return extract_text_from_image(file_path), 200
        elif file_extension == ".docx":
            return (
                extract_text_and_images_from_docx(file_path)
                if enable_ocr
                else extract_text_from_docx(file_path)
            ), 200
        elif file_extension == ".txt":
            return extract_text_from_txt(file_path), 200
        else:
            return f"Unsupported file type: {file_extension}", 400
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return f"Error processing file {file_path}: {e}", 500


def save_text_to_file(text, output_path):
    """Save extracted text to a file."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        logger.info(f"Extracted text saved to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save text: {e}")
        raise


def process_file(file_path, output_dir, enable_ocr=False):
    """Process a single file."""
    try:
        logger.info(f"Processing file: {file_path}")
        text = extract_text(file_path, enable_ocr)
        if output_dir:
            output_file = Path(output_dir) / (Path(file_path).stem + "_extracted.txt")
            save_text_to_file(text, output_file)
        else:
            print(f"\nExtracted Text from {file_path}:\n{text}\n")
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")


def process_directory_concurrently(
    directory_path, output_dir, enable_ocr=False, max_workers=4
):
    """Process all supported files in a directory concurrently."""
    try:
        directory = Path(directory_path)
        if not directory.is_dir():
            raise NotADirectoryError(f"{directory_path} is not a valid directory.")

        files_to_process = [
            file_path
            for file_path in directory.iterdir()
            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS
        ]

        if not files_to_process:
            print("No supported files found in the directory.")
            return

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(
                    process_file, file_path, output_dir, enable_ocr
                ): file_path
                for file_path in files_to_process
            }

            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")

        print(f"Processed {len(files_to_process)} files.")
    except Exception as e:
        logger.error(f"Error processing directory {directory_path}: {e}")
        raise


def start(input_path, output_path, enable_ocr, max_workers):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        if Path(input_path).is_file():
            # Single file processing
            validate_file_exists(input_path)
            text = extract_text(input_path, enable_ocr)
            print(f"\nExtracted Text from {input_path}:\n{text}\n")

            if output_path:
                output_file = Path(output_path) / (
                    Path(input_path).stem + "_extracted.txt"
                )
                save_text_to_file(text, output_file)

        elif Path(input_path).is_dir():
            # Directory processing
            if output_path:
                Path(output_path).mkdir(parents=True, exist_ok=True)
            process_directory_concurrently(
                input_path, output_path, enable_ocr, max_workers
            )
        else:
            raise ValueError(f"Invalid input path: {input_path}")
    except Exception as e:
        logger.error(e)
        print(f"Error: {e}")


# def main():
#     """CLI entry point."""
#     parser = argparse.ArgumentParser(description="Extract text from documents")
#     parser.add_argument("input", type=str, help="Path to the input file or directory")
#     parser.add_argument(
#         "-o",
#         "--output",
#         type=str,
#         help="Directory to save extracted text files (optional)",
#     )
#     parser.add_argument(
#         "--enable-ocr", action="store_true", help="Enable OCR for images in PDFs"
#     )
#     parser.add_argument(
#         "-w",
#         "--workers",
#         type=int,
#         default=4,
#         help="Number of workers for parallel processing (default: 4)",
#     )

#     args = parser.parse_args()

#     input_path = args.input
#     output_path = args.output if args.output else "./test_data/extracted_text"
#     enable_ocr = args.enable_ocr
#     max_workers = args.workers

#     start(input_path, output_path, enable_ocr, max_workers)


# if __name__ == "__main__":
#     main()
