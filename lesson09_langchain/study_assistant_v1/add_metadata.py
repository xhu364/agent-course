from datetime import datetime


def add_metadata(data):
    summary = data["summary"]

    return {
        **data,
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "model": "gemini-2.5-flash-lite",
            "summary_length": len(summary),
            "word_count": len(summary.split()),
            "language": "English",
            "version": "1.0",
        },
    }
