"""Core translation functionality using Argos Translate."""

import argostranslate.package
import argostranslate.translate


class Translator:
    """Korean to English translator using Argos Translate."""

    def __init__(self):
        self._installed_languages = None
        self._translation = None

    def _get_translation(self):
        """Get or initialize the Korean→English translation."""
        if self._translation is None:
            installed_languages = argostranslate.translate.get_installed_languages()

            korean = next(
                (lang for lang in installed_languages if lang.code == "ko"), None
            )
            english = next(
                (lang for lang in installed_languages if lang.code == "en"), None
            )

            if korean is None or english is None:
                raise RuntimeError(
                    "Korean→English language pack not installed. "
                    "Run 'download-languages' or call setup.download_korean_english()"
                )

            self._translation = korean.get_translation(english)

        return self._translation

    def translate(self, text: str) -> str:
        """Translate Korean text to English.

        Args:
            text: Korean text to translate.

        Returns:
            Translated English text.
        """
        translation = self._get_translation()
        return translation.translate(text)

    def translate_batch(self, texts: list[str]) -> list[str]:
        """Translate multiple Korean texts to English.

        Args:
            texts: List of Korean texts to translate.

        Returns:
            List of translated English texts.
        """
        return [self.translate(text) for text in texts]


# Module-level convenience instance
_translator = None


def translate(text: str) -> str:
    """Translate Korean text to English.

    Convenience function using a shared Translator instance.

    Args:
        text: Korean text to translate.

    Returns:
        Translated English text.
    """
    global _translator
    if _translator is None:
        _translator = Translator()
    return _translator.translate(text)
