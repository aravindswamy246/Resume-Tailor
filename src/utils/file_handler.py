import aiofiles
from pathlib import Path
from typing import BinaryIO
import PyPDF2
import docx
from io import BytesIO


async def read_file_async(file_path: Path) -> str:
    """Read a file asynchronously."""
    async with aiofiles.open(file_path, 'r') as f:
        return await f.read()


def read_file(file_path: Path) -> str:
    """Synchronous file reading for backward compatibility."""
    return file_path.read_text()


def extract_text_from_pdf(file: BinaryIO) -> str:
    """Extract text from PDF file."""
    # Read the file content into BytesIO for compatibility
    content = file.read()
    file_like = BytesIO(content)

    pdf_reader = PyPDF2.PdfReader(file_like)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()


def extract_text_from_docx(file: BinaryIO) -> str:
    """Extract text from DOCX file."""
    # Read the file content into BytesIO for compatibility
    content = file.read()
    file_like = BytesIO(content)

    doc = docx.Document(file_like)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text.strip()


def extract_text_from_txt(file: BinaryIO) -> str:
    """Extract text from TXT file."""
    content = file.read()
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    return content.strip()


async def extract_text_from_file(file: BinaryIO, filename: str) -> str:
    """
    Extract text from uploaded file based on extension.

    Args:
        file: Binary file object
        filename: Name of the file with extension

    Returns:
        Extracted text content

    Raises:
        ValueError: If file type is not supported
    """
    file_extension = Path(filename).suffix.lower()

    if file_extension == '.pdf':
        return extract_text_from_pdf(file)
    elif file_extension == '.docx':
        return extract_text_from_docx(file)
    elif file_extension == '.txt':
        return extract_text_from_txt(file)
    else:
        raise ValueError(
            f"Unsupported file type: {file_extension}. Supported types: .txt, .pdf, .docx")
