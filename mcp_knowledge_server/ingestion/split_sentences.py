"""split text into sentences"""

import re
from pathlib import Path


def split_sentences(text: str) -> list[str]:
    """Split text into reasonably sized sentences."""
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
    ]

    sentences = [
        part.strip()
        for paragraph in paragraphs
        for part in re.split(r"(?<=[.!?])\s+", paragraph)
        if part.strip()
    ]
    return sentences
