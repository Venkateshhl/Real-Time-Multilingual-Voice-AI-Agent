from langdetect import detect


def detect_language(text: str) -> str:
    """
    Detect the language code for the given text.
    Returns ISO 639-1 codes like 'en', 'hi', 'ta'.
    """
    try:
        return detect(text)
    except Exception:
        return "en"

