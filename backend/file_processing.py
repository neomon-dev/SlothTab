import os
import hashlib
import asyncio
import re
import mimetypes
from typing import Optional, Tuple, List, Dict, Any, BinaryIO
from pathlib import Path


def compute_file_hash(filepath: str) -> str:
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_file_info(filepath: str) -> Dict[str, Any]:
    """Get basic file information: size, type, hash."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    stat = os.stat(filepath)
    file_size = stat.st_size

    # Compute hash
    file_hash = compute_file_hash(filepath)

    # Get mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    mime_type = mime_type or "application/octet-stream"

    # Get extension
    ext = Path(filepath).suffix.lower()
    if not ext:
        ext = ""

    return {
        "filepath": filepath,
        "size": file_size,
        "hash": file_hash,
        "mime_type": mime_type,
        "extension": ext,
        "filename": os.path.basename(filepath),
    }


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename to be filesystem-safe."""
    # Remove or replace problematic characters
    filename = filename.strip()

    # Replace problematic characters
    replacements = {
        "/": "-",
        "\\": "-",
        ":": "-",
        "*": "",
        "?": "",
        '"': "",
        "<": "",
        ">": "",
        "|": "-",
    }

    for bad, good in replacements.items():
        filename = filename.replace(bad, good)

    # Remove multiple spaces/dots
    filename = re_filename = re.sub(r'\s+', ' ', filename).strip()
    filename = re.sub(r'\.+', '.', filename)

    # Ensure filename is not empty
    if not filename:
        filename = "untitled"

    # Limit length (leave room for extension)
    name_part, ext_part = os.path.splitext(filename)
    if len(name_part) > 100:
        name_part = name_part[:100]
    filename = name_part + ext_part

    return filename


def extract_text_from_pdf(filepath: str) -> Tuple[Optional[str], str]:
    """Extract text from a PDF file using PyMuPDF.

    Returns (text, error_message). If successful, text is not None and error is empty.
    """
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        doc.close()
        return text[:10000], ""  # Cap at 10k chars
    except ImportError:
        return None, "PyMuPDF not installed. pip install pymupdf"
    except Exception as e:
        return None, f"Error extracting PDF: {str(e)}"


def extract_text_from_docx(filepath: str) -> Tuple[Optional[str], str]:
    """Extract text from a DOCX file using python-docx.

    Returns (text, error_message). If successful, text is not None and error is empty.
    """
    try:
        from docx import Document
        doc = Document(filepath)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text[:10000], ""  # Cap at 10k chars
    except ImportError:
        return None, "python-docx not installed. pip install python-docx"
    except Exception as e:
        return None, f"Error extracting DOCX: {str(e)}"


def extract_text_from_txt(filepath: str) -> Tuple[Optional[str], str]:
    """Extract text from a TXT file.

    Returns (text, error_message).
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        return text[:10000], ""  # Cap at 10k chars
    except Exception as e:
        return None, f"Error extracting TXT: {str(e)}"


def extract_text_from_md(filepath: str) -> Tuple[Optional[str], str]:
    """Extract text from a Markdown file.

    Returns (text, error_message).
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        return text[:10000], ""
    except Exception as e:
        return None, f"Error extracting MD: {str(e)}"


def extract_text_from_image(filepath: str) -> Tuple[Optional[str], str]:
    """Extract text from an image using OCR or return metadata.

    Tries Pillow first for basic metadata, then falls back to filename/extension.
    For vision-capable AI models, the image can be sent directly.

    Returns (extracted_text_or_metadata, error_message).
    """
    try:
        from PIL import Image
        img = Image.open(filepath)

        # Get basic metadata
        metadata_parts = [
            f"Filename: {os.path.basename(filepath)}",
            f"Format: {img.format}",
            f"Mode: {img.mode}",
            f"Size: {img.size}",
        ]

        # Try to get some additional info
        if hasattr(img, "tag_v2"):
            try:
                fmt_name = img.format.lower()
                metadata_parts.append(f"Format: {fmt_name}")
            except:
                pass

        img.close()

        return "\n".join(metadata_parts), ""

    except ImportError:
        return None, "Pillow not installed. pip install Pillow"
    except Exception as e:
        # If Pillow fails, try to get basic file info
        try:
            stat = os.stat(filepath)
            return (
                f"Filename: {os.path.basename(filepath)}; Size: {stat.st_size} bytes",
                "",
            )
        except Exception:
            return None, f"Error processing image: {str(e)}"


def get_supported_extensions() -> Dict[str, str]:
    """Return mapping of supported file extensions to their processing functions."""
    return {
        ".pdf": "pdf",
        ".docx": "docx",
        ".txt": "txt",
        ".md": "md",
        ".png": "image",
        ".jpg": "image",
        ".jpeg": "image",
        ".webp": "image",
    }


def get_processor_for_file(filepath: str) -> Tuple[Optional[str], str]:
    """Determine the appropriate processor for a file based on extension.

    Returns (processor_key, error_message). processor_key can be used
    to call the appropriate extraction function.
    """
    ext = os.path.splitext(filepath)[1].lower()

    processors = {
        ".pdf": extract_text_from_pdf,
        ".docx": extract_text_from_docx,
        ".txt": extract_text_from_txt,
        ".md": extract_text_from_md,
        ".png": extract_text_from_image,
        ".jpg": extract_text_from_image,
        ".jpeg": extract_text_from_image,
        ".webp": extract_text_from_image,
    }

    if ext in processors:
        return processors[ext], ""

    return None, f"Unsupported file type: {ext}"


async def process_file_async(
    filepath: str,
    ai_provider=None,
    analysis_prompt: str = "",
) -> Dict[str, Any]:
    """Process a file asynchronously: extract text and optionally analyze with AI.

    Returns a dict with:
    - file_info: basic file information
    - extracted_text: the text content
    - analysis: AI analysis result (if ai_provider and prompt provided)
    - error: any error message
    """
    # Get file info
    file_info = get_file_info(filepath)

    # Extract text based on type
    processor, error = get_processor_for_file(filepath)

    extracted_text = ""
    process_error = ""

    if processor:
        # Run sync extraction in a thread pool
        loop = asyncio.get_event_loop()
        extracted_text, process_error = await loop.run_in_executor(
            None, processor, filepath
        )
    else:
        process_error = error

    result = {
        "file_info": file_info,
        "extracted_text": extracted_text or "",
        "process_error": process_error,
        "analysis": None,
    }

    # Optionally run AI analysis
    if ai_provider and analysis_prompt and extracted_text:
        try:
            # Truncate text if too long
            text_to_analyze = extracted_text[:5000]
            messages = [
                {"role": "system", "content": "You are SlothTab, a file organization assistant."},
                {"role": "user", "content": analysis_prompt + "\n\nFile content: " + text_to_analyze},
            ]
            ai_response = await ai_provider.chat_complete(messages=messages)

            # Try to extract JSON from response
            content = ai_response.get("choices", [{}])[0].get("message", {}).get(
                "content", ""
            )

            # Simple JSON extraction
            import re
            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if json_match:
                try:
                    analysis_result = json.loads(json_match.group())
                    result["analysis"] = analysis_result
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            result["analysis_error"] = str(e)

    return result