"""Unit tests for LearningTracker."""

from datetime import timedelta

import pytest

from software_development_lessons.core import LearningTracker
from software_development_lessons.core.learning_tracker import (
    LearningProgress,
    ProgressStatus,
)


class TestLearningProgress:
    """Test cases for LearningProgress."""

    def test_progress_initialization(self) -> None:
        """Test creating a new learning progress."""
        progress = LearningProgress(resource_url="https://example.com")

        assert progress.resource_url == "https://example.com"
        assert progress.status == ProgressStatus.NOT_STARTED
        assert progress.completion_percentage == 0
        assert len(progress.sessions) == 0

    def test_start_session(self) -> None:
        """Test starting a new learning session."""
        progress = LearningProgress(resource_url="https://example.com")
        session = progress.start_session()

        assert progress.status == ProgressStatus.IN_PROGRESS
        assert len(progress.sessions) == 1
        assert session.resource_url == "https://example.com"
        assert progress.started_at is not None

    def test_update_progress_valid(self) -> None:
        """Test updating progress with valid percentage."""
        progress = LearningProgress(resource_url="https://example.com")

        progress.update_progress(50)
        assert progress.completion_percentage == 50
        assert progress.status == ProgressStatus.IN_PROGRESS

        progress.update_progress(100)
        assert progress.completion_percentage == 100
        assert progress.status == ProgressStatus.COMPLETED
        assert progress.completed_at is not None

    def test_update_progress_invalid(self) -> None:
        """Test that invalid percentage raises ValueError."""
        progress = LearningProgress(resource_url="https://example.com")

        with pytest.raises(ValueError, match="between 0 and 100"):
            progress.update_progress(150)

        with pytest.raises(ValueError, match="between 0 and 100"):
            progress.update_progress(-10)

    def test_total_time_spent(self) -> None:
        """Test calculating total time spent."""
        progress = LearningProgress(resource_url="https://example.com")

        session1 = progress.start_session()
        session1.complete()

        session2 = progress.start_session()
        session2.complete()

        total_time = progress.total_time_spent
        assert isinstance(total_time, timedelta)
        assert total_time.total_seconds() >= 0

    def test_to_dict(self) -> None:
        """Test converting progress to dictionary."""
        progress = LearningProgress(resource_url="https://example.com")
        progress.start_session()
        progress.update_progress(75)

        result = progress.to_dict()

        assert result["resource_url"] == "https://example.com"
        assert result["status"] == "in_progress"
        assert result["completion_percentage"] == 75
        assert result["total_sessions"] == 1
        assert "total_time_hours" in result


class TestLearningTracker:
    """Test cases for LearningTracker."""

    def test_initialization(self, learning_tracker: LearningTracker) -> None:
        """Test LearningTracker initialization."""
        assert learning_tracker.get_all_progress() == []

    def test_start_learning(self, learning_tracker: LearningTracker) -> None:
        """Test starting to learn a new resource."""
        url = "https://example.com/course"
        session = learning_tracker.start_learning(url)

        assert session.resource_url == url
        progress = learning_tracker.get_progress(url)
        assert progress is not None
        assert progress.status == ProgressStatus.IN_PROGRESS

    def test_update_progress(self, learning_tracker: LearningTracker) -> None:
        """Test updating learning progress."""
        url = "https://example.com/course"
        learning_tracker.start_learning(url)
        learning_tracker.update_progress(url, 50)

        progress = learning_tracker.get_progress(url)
        assert progress is not None
        assert progress.completion_percentage == 50

    def test_update_progress_nonexistent(self, learning_tracker: LearningTracker) -> None:
        """Test that updating nonexistent resource raises KeyError."""
        with pytest.raises(KeyError, match="not being tracked"):
            learning_tracker.update_progress("https://nonexistent.com", 50)

    def test_get_progress(self, learning_tracker: LearningTracker) -> None:
        """Test getting progress for a specific resource."""
        url = "https://example.com/course"
        learning_tracker.start_learning(url)

        progress = learning_tracker.get_progress(url)
        assert progress is not None
        assert progress.resource_url == url

        # Test nonexistent resource
        assert learning_tracker.get_progress("https://nonexistent.com") is None

    def test_get_completed_resources(self, learning_tracker: LearningTracker) -> None:
        """Test getting completed resources."""
        url1 = "https://example.com/course1"
        url2 = "https://example.com/course2"
        url3 = "https://example.com/course3"

        learning_tracker.start_learning(url1)
        learning_tracker.update_progress(url1, 100)

        learning_tracker.start_learning(url2)
        learning_tracker.update_progress(url2, 50)

        learning_tracker.start_learning(url3)
        learning_tracker.update_progress(url3, 100)

        completed = learning_tracker.get_completed_resources()
        assert len(completed) == 2
        assert all(p.status == ProgressStatus.COMPLETED for p in completed)

    def test_get_in_progress_resources(self, learning_tracker: LearningTracker) -> None:
        """Test getting in-progress resources."""
        url1 = "https://example.com/course1"
        url2 = "https://example.com/course2"

        learning_tracker.start_learning(url1)
        learning_tracker.update_progress(url1, 100)

        learning_tracker.start_learning(url2)
        learning_tracker.update_progress(url2, 50)

        in_progress = learning_tracker.get_in_progress_resources()
        assert len(in_progress) == 1
        assert in_progress[0].resource_url == url2

    def test_get_total_time_spent(self, learning_tracker: LearningTracker) -> None:
        """Test calculating total time spent across all resources."""
        url1 = "https://example.com/course1"
        url2 = "https://example.com/course2"

        session1 = learning_tracker.start_learning(url1)
        session1.complete()

        session2 = learning_tracker.start_learning(url2)
        session2.complete()

        total_time = learning_tracker.get_total_time_spent()
        assert isinstance(total_time, timedelta)
        assert total_time.total_seconds() >= 0

    def test_get_statistics(self, learning_tracker: LearningTracker) -> None:
        """Test getting learning statistics."""
        # Add some sample progress
        learning_tracker.start_learning("https://example.com/1")
        learning_tracker.update_progress("https://example.com/1", 100)

        learning_tracker.start_learning("https://example.com/2")
        learning_tracker.update_progress("https://example.com/2", 50)

        learning_tracker.start_learning("https://example.com/3")

        stats = learning_tracker.get_statistics()

        assert stats["total_resources"] == 3
        assert stats["completed"] == 1
        assert stats["in_progress"] == 2
        assert 0 <= stats["average_completion"] <= 100
        assert stats["total_hours_spent"] >= 0
