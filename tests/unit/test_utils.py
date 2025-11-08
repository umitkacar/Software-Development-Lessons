"""Unit tests for utility functions."""

from datetime import timedelta

import pytest

from software_development_lessons.utils import format_duration, validate_url


class TestValidateUrl:
    """Test cases for validate_url function."""

    @pytest.mark.parametrize(
        "url,expected",
        [
            ("https://example.com", True),
            ("http://example.com", True),
            ("https://example.com/path", True),
            ("https://example.com:8080/path", True),
            ("not-a-url", False),
            ("ftp://example.com", False),
            ("", False),
            ("javascript:alert(1)", False),
        ],
    )
    def test_validate_url(self, url: str, expected: bool) -> None:
        """Test URL validation with various inputs."""
        assert validate_url(url) == expected


class TestFormatDuration:
    """Test cases for format_duration function."""

    def test_format_hours_and_minutes(self) -> None:
        """Test formatting hours and minutes."""
        duration = timedelta(hours=2, minutes=30)
        assert format_duration(duration) == "2h 30m"

    def test_format_minutes_and_seconds(self) -> None:
        """Test formatting minutes and seconds."""
        duration = timedelta(minutes=45, seconds=30)
        assert format_duration(duration) == "45m 30s"

    def test_format_only_hours(self) -> None:
        """Test formatting only hours."""
        duration = timedelta(hours=3)
        assert format_duration(duration) == "3h"

    def test_format_only_seconds(self) -> None:
        """Test formatting only seconds."""
        duration = timedelta(seconds=45)
        assert format_duration(duration) == "45s"

    def test_format_zero_duration(self) -> None:
        """Test formatting zero duration."""
        duration = timedelta()
        assert format_duration(duration) == "0s"

    def test_format_complex_duration(self) -> None:
        """Test formatting complex duration."""
        duration = timedelta(hours=1, minutes=23, seconds=45)
        assert format_duration(duration) == "1h 23m 45s"
