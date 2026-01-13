"""PDF text extraction and chunking for translation."""

from pathlib import Path

import pdfplumber


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract all text from a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text from all pages.
    """
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n\n".join(text_parts)


def chunk_text(text: str, max_chars: int = 2000) -> list[str]:
    """Split text into chunks suitable for translation.

    Chunks at paragraph boundaries when possible, falling back to
    sentence boundaries for very long paragraphs.

    Args:
        text: Text to chunk.
        max_chars: Maximum characters per chunk.

    Returns:
        List of text chunks.
    """
    if not text.strip():
        return []

    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_len = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # If paragraph itself exceeds max_chars, split by sentences
        if len(para) > max_chars:
            # Save current chunk first
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_len = 0

            # Split long paragraph by sentences
            sentences = _split_sentences(para)
            for sentence in sentences:
                if current_len + len(sentence) > max_chars and current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_len = 0
                current_chunk.append(sentence)
                current_len += len(sentence)

            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_len = 0
            continue

        # Normal case: add paragraph to current chunk
        if current_len + len(para) > max_chars and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = []
            current_len = 0

        current_chunk.append(para)
        current_len += len(para)

    # Don't forget the last chunk
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences (basic implementation).

    Handles common sentence endings: . ! ? and Korean period.

    Args:
        text: Text to split.

    Returns:
        List of sentences.
    """
    import re

    # Split on sentence-ending punctuation followed by space or end
    sentences = re.split(r'(?<=[.!?。])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def extract_and_chunk_pdf(
    pdf_path: str | Path,
    max_chars: int = 2000,
) -> list[str]:
    """Extract text from PDF and split into translatable chunks.

    Args:
        pdf_path: Path to the PDF file.
        max_chars: Maximum characters per chunk.

    Returns:
        List of text chunks ready for translation.
    """
    text = extract_text_from_pdf(pdf_path)
    return chunk_text(text, max_chars)
