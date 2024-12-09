from pathlib import Path


def get_file_extension(file_path):
    """Get the file extension."""
    return Path(file_path).suffix.lower()


def validate_file_exists(file_path):
    """Check if the file exists."""
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
