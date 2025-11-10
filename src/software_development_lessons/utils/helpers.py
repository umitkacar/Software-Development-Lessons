"""Helper utilities for the application."""

from datetime import timedelta
from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    """Validate if a string is a valid URL.

    Args:
        url: The URL string to validate.

    Returns:
        True if the URL is valid, False otherwise.

    Examples:
        >>> validate_url("https://example.com")
        True
        >>> validate_url("not-a-url")
        False
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ("http", "https")
    except (ValueError, AttributeError):
        return False


def format_duration(duration: timedelta) -> str:
    """Format a timedelta into a human-readable string.

    Args:
        duration: The timedelta to format.

    Returns:
        A formatted string like "2h 30m" or "45m 30s".

    Examples:
        >>> from datetime import timedelta
        >>> format_duration(timedelta(hours=2, minutes=30))
        '2h 30m'
        >>> format_duration(timedelta(minutes=45, seconds=30))
        '45m 30s'
    """
    total_seconds = int(duration.total_seconds())

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)
