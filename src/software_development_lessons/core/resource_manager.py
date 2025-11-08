"""Resource Manager for managing learning resources."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class ResourceCategory(Enum):
    """Categories for learning resources."""

    AI_ML = "ai_ml"
    WEB_DEV = "web_dev"
    CLOUD_DEVOPS = "cloud_devops"
    MOBILE = "mobile"
    WEB3 = "web3"
    DATA_SCIENCE = "data_science"
    GAME_DEV = "game_dev"
    CYBERSECURITY = "cybersecurity"


class DifficultyLevel(Enum):
    """Difficulty levels for resources."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class Resource:
    """Represents a learning resource.

    Attributes:
        title: The title of the resource.
        url: The URL to access the resource.
        category: The category this resource belongs to.
        difficulty: The difficulty level of the resource.
        description: A brief description of the resource.
        tags: Optional tags for better categorization.
        is_free: Whether the resource is free to access.
    """

    title: str
    url: str
    category: ResourceCategory
    difficulty: DifficultyLevel
    description: str
    tags: list[str] | None = None
    is_free: bool = True

    def __post_init__(self) -> None:
        """Validate resource data after initialization."""
        if not self.title:
            msg = "Resource title cannot be empty"
            raise ValueError(msg)
        if not self.url.startswith(("http://", "https://")):
            msg = "Resource URL must start with http:// or https://"
            raise ValueError(msg)

    def to_dict(self) -> dict[str, Any]:
        """Convert resource to dictionary representation.

        Returns:
            Dictionary containing resource data.
        """
        return {
            "title": self.title,
            "url": self.url,
            "category": self.category.value,
            "difficulty": self.difficulty.value,
            "description": self.description,
            "tags": self.tags or [],
            "is_free": self.is_free,
        }


class ResourceManager:
    """Manages a collection of learning resources.

    This class provides methods to add, remove, search, and filter
    learning resources across different categories and difficulty levels.
    """

    def __init__(self) -> None:
        """Initialize the ResourceManager with an empty collection."""
        self._resources: list[Resource] = []

    def add_resource(self, resource: Resource) -> None:
        """Add a new resource to the collection.

        Args:
            resource: The resource to add.

        Raises:
            ValueError: If the resource already exists.
        """
        if any(r.url == resource.url for r in self._resources):
            msg = f"Resource with URL {resource.url} already exists"
            raise ValueError(msg)
        self._resources.append(resource)

    def remove_resource(self, url: str) -> bool:
        """Remove a resource by its URL.

        Args:
            url: The URL of the resource to remove.

        Returns:
            True if the resource was removed, False if not found.
        """
        original_length = len(self._resources)
        self._resources = [r for r in self._resources if r.url != url]
        return len(self._resources) < original_length

    def get_by_category(self, category: ResourceCategory) -> list[Resource]:
        """Get all resources in a specific category.

        Args:
            category: The category to filter by.

        Returns:
            List of resources in the specified category.
        """
        return [r for r in self._resources if r.category == category]

    def get_by_difficulty(self, difficulty: DifficultyLevel) -> list[Resource]:
        """Get all resources at a specific difficulty level.

        Args:
            difficulty: The difficulty level to filter by.

        Returns:
            List of resources at the specified difficulty level.
        """
        return [r for r in self._resources if r.difficulty == difficulty]

    def search_by_tag(self, tag: str) -> list[Resource]:
        """Search resources by tag.

        Args:
            tag: The tag to search for.

        Returns:
            List of resources containing the specified tag.
        """
        return [r for r in self._resources if r.tags and tag in r.tags]

    def get_free_resources(self) -> list[Resource]:
        """Get all free resources.

        Returns:
            List of free resources.
        """
        return [r for r in self._resources if r.is_free]

    def get_all(self) -> list[Resource]:
        """Get all resources.

        Returns:
            List of all resources.
        """
        return self._resources.copy()

    def count(self) -> int:
        """Get the total number of resources.

        Returns:
            The total count of resources.
        """
        return len(self._resources)

    def export_to_json(self, file_path: Path) -> None:
        """Export resources to a JSON file.

        Args:
            file_path: The path to save the JSON file.
        """
        import json

        data = [r.to_dict() for r in self._resources]
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
