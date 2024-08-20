""" This module contains mappings between language codes and writing systems. """

# Supported writing systems: 'ch', 'en', 'korean', 'japan', 'chinese_cht', 'ta', 'te', 'ka', 'latin',
# 'arabic', 'cyrillic', or 'devanagari'
language_to_writing_system = {
    "zh": "ch",  # Chinese (Simplified)
    "zh-Hant": "chinese_cht",  # Chinese (Traditional)
    "en": "latin",  # English
    "ko": "korean",  # Korean
    "ja": "japan",  # Japanese
    "ta": "ta",  # Tamil
    "te": "te",  # Telugu
    "ka": "ka",  # Georgian
    "la": "latin",  # Latin
    "ar": "arabic",  # Arabic
    "ru": "cyrillic",  # Russian
    "hi": "devanagari",  # Hindi
    "mr": "devanagari",  # Marathi
    "ne": "devanagari",  # Nepali
    "af": "latin",  # Afrikaans
    "sq": "latin",  # Albanian
    "az": "latin",  # Azerbaijani
    "eu": "latin",  # Basque
    "be": "cyrillic",  # Belarusian
    "bs": "latin",  # Bosnian
    "bg": "cyrillic",  # Bulgarian
    "ca": "latin",  # Catalan
    "hr": "latin",  # Croatian
    "cs": "latin",  # Czech
    "da": "latin",  # Danish
    "nl": "latin",  # Dutch
    "et": "latin",  # Estonian
    "fo": "latin",  # Faroese
    "fi": "latin",  # Finnish
    "fr": "latin",  # French
    "gl": "latin",  # Galician
    "de": "latin",  # German
    "hu": "latin",  # Hungarian
    "is": "latin",  # Icelandic
    "id": "latin",  # Indonesian
    "ga": "latin",  # Irish
    "it": "latin",  # Italian
    "kk": "cyrillic",  # Kazakh
    "lv": "latin",  # Latvian
    "lt": "latin",  # Lithuanian
    "lb": "latin",  # Luxembourgish
    "mk": "cyrillic",  # Macedonian
    "ms": "latin",  # Malay
    "mt": "latin",  # Maltese
    "mn": "cyrillic",  # Mongolian
    "no": "latin",  # Norwegian
    "fa": "arabic",  # Persian
    "pl": "latin",  # Polish
    "pt": "latin",  # Portuguese
    "ro": "latin",  # Romanian
    "sr": "cyrillic",  # Serbian
    "sk": "latin",  # Slovak
    "sl": "latin",  # Slovenian
    "es": "latin",  # Spanish
    "sw": "latin",  # Swahili
    "sv": "latin",  # Swedish
    "th": "thai",  # Thai (Note: Not in specified list)
    "tr": "latin",  # Turkish
    "uk": "cyrillic",  # Ukrainian
    "ur": "arabic",  # Urdu
    "uz": "latin",  # Uzbek
    "vi": "latin",  # Vietnamese
    "cy": "latin",  # Welsh
    "xh": "latin",  # Xhosa
    "zu": "latin",  # Zulu
}


def get_writing_system(language_code: str) -> str:
    """
    Returns the writing system associated with the given language code.

    Args:
        language_code (str): The language code for which to retrieve the writing system.

    Returns:
        str: The writing system associated with the language code, or 'Unknown' if not found.
    """
    return language_to_writing_system.get(language_code, "Unknown")
