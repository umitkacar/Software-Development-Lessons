"""Pytest configuration and fixtures."""

import pytest

from software_development_lessons.core import LearningTracker, ResourceManager
from software_development_lessons.core.resource_manager import (
    DifficultyLevel,
    Resource,
    ResourceCategory,
)


@pytest.fixture
def resource_manager() -> ResourceManager:
    """Create a fresh ResourceManager instance for testing.

    Returns:
        A new ResourceManager instance.
    """
    return ResourceManager()


@pytest.fixture
def learning_tracker() -> LearningTracker:
    """Create a fresh LearningTracker instance for testing.

    Returns:
        A new LearningTracker instance.
    """
    return LearningTracker()


@pytest.fixture
def sample_resource() -> Resource:
    """Create a sample resource for testing.

    Returns:
        A sample Resource instance.
    """
    return Resource(
        title="Test Resource",
        url="https://example.com/test",
        category=ResourceCategory.AI_ML,
        difficulty=DifficultyLevel.BEGINNER,
        description="A test resource for unit testing",
        tags=["test", "example"],
        is_free=True,
    )


@pytest.fixture
def sample_resources() -> list[Resource]:
    """Create a list of sample resources for testing.

    Returns:
        A list of sample Resource instances.
    """
    return [
        Resource(
            title="PyTorch Tutorial",
            url="https://pytorch.org/tutorials/",
            category=ResourceCategory.AI_ML,
            difficulty=DifficultyLevel.INTERMEDIATE,
            description="Official PyTorch tutorials",
            tags=["pytorch", "deep-learning"],
        ),
        Resource(
            title="Next.js Docs",
            url="https://nextjs.org/learn",
            category=ResourceCategory.WEB_DEV,
            difficulty=DifficultyLevel.BEGINNER,
            description="Learn Next.js framework",
            tags=["react", "nextjs"],
        ),
        Resource(
            title="Kubernetes Guide",
            url="https://kubernetes.io/docs/",
            category=ResourceCategory.CLOUD_DEVOPS,
            difficulty=DifficultyLevel.ADVANCED,
            description="Kubernetes documentation",
            tags=["kubernetes", "devops"],
        ),
    ]
