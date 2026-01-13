"""Command-line interface for Korean→English translation."""

import argparse
import sys

from transylvania.translator import Translator
from transylvania.setup import check_installation, download_korean_english


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

    # Get text to translate
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
