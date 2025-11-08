"""Learning Progress Tracker for monitoring educational journey."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any


class ProgressStatus(Enum):
    """Status of learning progress."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"


@dataclass
class LearningSession:
    """Represents a single learning session.

    Attributes:
        resource_url: URL of the resource being studied.
        start_time: When the session started.
        end_time: When the session ended (None if ongoing).
        notes: Optional notes about the session.
    """

    resource_url: str
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    notes: str = ""

    @property
    def duration(self) -> timedelta:
        """Calculate the duration of the session.

        Returns:
            The duration of the session, or time elapsed if still ongoing.
        """
        end = self.end_time or datetime.now()
        return end - self.start_time

    def complete(self, notes: str = "") -> None:
        """Mark the session as complete.

        Args:
            notes: Optional notes to add when completing the session.
        """
        self.end_time = datetime.now()
        if notes:
            self.notes = notes


@dataclass
class LearningProgress:
    """Tracks progress for a specific resource.

    Attributes:
        resource_url: URL of the resource.
        status: Current progress status.
        completion_percentage: Percentage of completion (0-100).
        sessions: List of learning sessions.
        started_at: When learning started.
        completed_at: When learning was completed.
    """

    resource_url: str
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    completion_percentage: int = 0
    sessions: list[LearningSession] = field(default_factory=list)
    started_at: datetime | None = None
    completed_at: datetime | None = None

    def start_session(self) -> LearningSession:
        """Start a new learning session.

        Returns:
            The newly created learning session.
        """
        if self.status == ProgressStatus.NOT_STARTED:
            self.status = ProgressStatus.IN_PROGRESS
            self.started_at = datetime.now()

        session = LearningSession(resource_url=self.resource_url)
        self.sessions.append(session)
        return session

    def update_progress(self, percentage: int) -> None:
        """Update the completion percentage.

        Args:
            percentage: New completion percentage (0-100).

        Raises:
            ValueError: If percentage is not between 0 and 100.
        """
        if not 0 <= percentage <= 100:
            msg = "Percentage must be between 0 and 100"
            raise ValueError(msg)

        self.completion_percentage = percentage

        if percentage == 100:
            self.status = ProgressStatus.COMPLETED
            self.completed_at = datetime.now()
        elif percentage > 0:
            self.status = ProgressStatus.IN_PROGRESS

    @property
    def total_time_spent(self) -> timedelta:
        """Calculate total time spent on this resource.

        Returns:
            Total time spent across all sessions.
        """
        return sum((session.duration for session in self.sessions), timedelta())

    def to_dict(self) -> dict[str, Any]:
        """Convert progress to dictionary representation.

        Returns:
            Dictionary containing progress data.
        """
        return {
            "resource_url": self.resource_url,
            "status": self.status.value,
            "completion_percentage": self.completion_percentage,
            "total_sessions": len(self.sessions),
            "total_time_hours": self.total_time_spent.total_seconds() / 3600,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class LearningTracker:
    """Tracks learning progress across multiple resources.

    This class provides methods to track learning sessions, monitor progress,
    and generate statistics about the learning journey.
    """

    def __init__(self) -> None:
        """Initialize the LearningTracker with empty progress tracking."""
        self._progress: dict[str, LearningProgress] = {}

    def start_learning(self, resource_url: str) -> LearningSession:
        """Start learning a new resource.

        Args:
            resource_url: URL of the resource to start learning.

        Returns:
            The newly created learning session.
        """
        if resource_url not in self._progress:
            self._progress[resource_url] = LearningProgress(resource_url=resource_url)

        return self._progress[resource_url].start_session()

    def update_progress(self, resource_url: str, percentage: int) -> None:
        """Update progress for a specific resource.

        Args:
            resource_url: URL of the resource.
            percentage: New completion percentage (0-100).

        Raises:
            KeyError: If the resource is not being tracked.
        """
        if resource_url not in self._progress:
            msg = f"Resource {resource_url} is not being tracked"
            raise KeyError(msg)

        self._progress[resource_url].update_progress(percentage)

    def get_progress(self, resource_url: str) -> LearningProgress | None:
        """Get progress for a specific resource.

        Args:
            resource_url: URL of the resource.

        Returns:
            The learning progress, or None if not found.
        """
        return self._progress.get(resource_url)

    def get_all_progress(self) -> list[LearningProgress]:
        """Get progress for all resources.

        Returns:
            List of all learning progress records.
        """
        return list(self._progress.values())

    def get_completed_resources(self) -> list[LearningProgress]:
        """Get all completed resources.

        Returns:
            List of completed learning progress records.
        """
        return [p for p in self._progress.values() if p.status == ProgressStatus.COMPLETED]

    def get_in_progress_resources(self) -> list[LearningProgress]:
        """Get all in-progress resources.

        Returns:
            List of in-progress learning progress records.
        """
        return [p for p in self._progress.values() if p.status == ProgressStatus.IN_PROGRESS]

    def get_total_time_spent(self) -> timedelta:
        """Calculate total time spent learning across all resources.

        Returns:
            Total time spent learning.
        """
        return sum((p.total_time_spent for p in self._progress.values()), timedelta())

    def get_statistics(self) -> dict[str, Any]:
        """Get learning statistics.

        Returns:
            Dictionary containing various learning statistics.
        """
        all_progress = self._progress.values()
        completed = self.get_completed_resources()
        in_progress = self.get_in_progress_resources()

        return {
            "total_resources": len(self._progress),
            "completed": len(completed),
            "in_progress": len(in_progress),
            "average_completion": (
                sum(p.completion_percentage for p in all_progress) / len(all_progress)
                if all_progress
                else 0
            ),
            "total_hours_spent": self.get_total_time_spent().total_seconds() / 3600,
        }
