"""Setup utilities for downloading Argos Translate language packs."""

import argostranslate.package
import argostranslate.translate


def download_korean_english() -> None:
    """Download and install the Korean→English language pack.

    This function downloads the latest package index and installs
    the Korean to English translation model.
    """
    print("Updating Argos Translate package index...")
    argostranslate.package.update_package_index()

    available_packages = argostranslate.package.get_available_packages()

    # Find Korean→English package
    ko_en_package = next(
        (
            pkg
            for pkg in available_packages
            if pkg.from_code == "ko" and pkg.to_code == "en"
        ),
        None,
    )

    if ko_en_package is None:
        raise RuntimeError("Korean→English package not found in available packages")

    print(f"Downloading Korean→English package: {ko_en_package}")
    download_path = ko_en_package.download()

    print("Installing package...")
    argostranslate.package.install_from_path(download_path)

    print("Korean→English translation pack installed successfully!")


def check_installation() -> bool:
    """Check if Korean→English translation is installed.

    Returns:
        True if the language pack is installed, False otherwise.
    """
    installed_languages = argostranslate.translate.get_installed_languages()

    korean = next(
        (lang for lang in installed_languages if lang.code == "ko"), None
    )
    english = next(
        (lang for lang in installed_languages if lang.code == "en"), None
    )

    if korean is None or english is None:
        return False

    # Check if translation exists
    translation = korean.get_translation(english)
    return translation is not None


def list_installed_languages() -> list[str]:
    """List all installed language codes.

    Returns:
        List of installed language codes.
    """
    installed_languages = argostranslate.translate.get_installed_languages()
    return [lang.code for lang in installed_languages]


if __name__ == "__main__":
    download_korean_english()
