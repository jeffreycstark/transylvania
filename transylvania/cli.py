"""Command-line interface for Korean→English translation."""

import argparse
import sys
from pathlib import Path

from transylvania.translator import Translator
from transylvania.setup import check_installation, download_korean_english


def translate_pdf_file(pdf_path: str, output_path: str | None = None) -> int:
    """Translate a PDF file from Korean to English.

    Args:
        pdf_path: Path to the Korean PDF.
        output_path: Optional path for output file. Prints to stdout if None.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    from transylvania.pdf import extract_and_chunk_pdf

    path = Path(pdf_path)
    if not path.exists():
        print(f"Error: File not found: {pdf_path}", file=sys.stderr)
        return 1

    if not path.suffix.lower() == ".pdf":
        print(f"Error: Not a PDF file: {pdf_path}", file=sys.stderr)
        return 1

    try:
        chunks = extract_and_chunk_pdf(path)
        if not chunks:
            print("Error: No text found in PDF", file=sys.stderr)
            return 1

        print(f"Extracted {len(chunks)} chunks from PDF", file=sys.stderr)

        translator = Translator()
        translated_chunks = []

        for i, chunk in enumerate(chunks, 1):
            print(f"Translating chunk {i}/{len(chunks)}...", file=sys.stderr)
            translated_chunks.append(translator.translate(chunk))

        result = "\n\n".join(translated_chunks)

        if output_path:
            Path(output_path).write_text(result, encoding="utf-8")
            print(f"Translation saved to: {output_path}", file=sys.stderr)
        else:
            print(result)

        return 0

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error processing PDF: {e}", file=sys.stderr)
        return 1


def main() -> int:
    """Main CLI entry point for translation."""
    parser = argparse.ArgumentParser(
        description="Translate Korean text to English using Argos Translate"
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Korean text to translate (reads from stdin if not provided)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if language pack is installed",
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Download and install the Korean→English language pack",
    )
    parser.add_argument(
        "--pdf",
        metavar="FILE",
        help="Translate a PDF file instead of text",
    )
    parser.add_argument(
        "--output", "-o",
        metavar="FILE",
        help="Output file for PDF translation (prints to stdout if not specified)",
    )

    args = parser.parse_args()

    if args.install:
        download_korean_english()
        return 0

    if args.check:
        if check_installation():
            print("Korean→English translation pack is installed.")
            return 0
        else:
            print("Korean→English translation pack is NOT installed.")
            print("Run: translate --install")
            return 1

    # PDF translation mode
    if args.pdf:
        return translate_pdf_file(args.pdf, args.output)

    # Text translation mode
    if args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    else:
        parser.print_help()
        return 1

    if not text:
        print("No text provided", file=sys.stderr)
        return 1

    try:
        translator = Translator()
        result = translator.translate(text)
        print(result)
        return 0
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
