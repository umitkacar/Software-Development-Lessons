"""Unit tests for ResourceManager."""

from pathlib import Path

import pytest

from software_development_lessons.core import ResourceManager
from software_development_lessons.core.resource_manager import (
    DifficultyLevel,
    Resource,
    ResourceCategory,
)


class TestResource:
    """Test cases for Resource dataclass."""

    def test_resource_creation(self, sample_resource: Resource) -> None:
        """Test creating a valid resource."""
        assert sample_resource.title == "Test Resource"
        assert sample_resource.url == "https://example.com/test"
        assert sample_resource.category == ResourceCategory.AI_ML
        assert sample_resource.difficulty == DifficultyLevel.BEGINNER
        assert sample_resource.is_free is True

    def test_resource_validation_empty_title(self) -> None:
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="title cannot be empty"):
            Resource(
                title="",
                url="https://example.com",
                category=ResourceCategory.WEB_DEV,
                difficulty=DifficultyLevel.BEGINNER,
                description="Test",
            )

    def test_resource_validation_invalid_url(self) -> None:
        """Test that invalid URL raises ValueError."""
        with pytest.raises(ValueError, match="must start with http"):
            Resource(
                title="Test",
                url="invalid-url",
                category=ResourceCategory.WEB_DEV,
                difficulty=DifficultyLevel.BEGINNER,
                description="Test",
            )

    def test_resource_to_dict(self, sample_resource: Resource) -> None:
        """Test converting resource to dictionary."""
        result = sample_resource.to_dict()

        assert result["title"] == "Test Resource"
        assert result["url"] == "https://example.com/test"
        assert result["category"] == "ai_ml"
        assert result["difficulty"] == "beginner"
        assert result["is_free"] is True
        assert "test" in result["tags"]


class TestResourceManager:
    """Test cases for ResourceManager."""

    def test_initialization(self, resource_manager: ResourceManager) -> None:
        """Test ResourceManager initialization."""
        assert resource_manager.count() == 0
        assert resource_manager.get_all() == []

    def test_add_resource(
        self, resource_manager: ResourceManager, sample_resource: Resource
    ) -> None:
        """Test adding a resource."""
        resource_manager.add_resource(sample_resource)

        assert resource_manager.count() == 1
        assert sample_resource in resource_manager.get_all()

    def test_add_duplicate_resource(
        self, resource_manager: ResourceManager, sample_resource: Resource
    ) -> None:
        """Test that adding duplicate resource raises ValueError."""
        resource_manager.add_resource(sample_resource)

        with pytest.raises(ValueError, match="already exists"):
            resource_manager.add_resource(sample_resource)

    def test_remove_resource(
        self, resource_manager: ResourceManager, sample_resource: Resource
    ) -> None:
        """Test removing a resource."""
        resource_manager.add_resource(sample_resource)
        result = resource_manager.remove_resource(sample_resource.url)

        assert result is True
        assert resource_manager.count() == 0

    def test_remove_nonexistent_resource(self, resource_manager: ResourceManager) -> None:
        """Test removing a resource that doesn't exist."""
        result = resource_manager.remove_resource("https://nonexistent.com")

        assert result is False

    def test_get_by_category(
        self, resource_manager: ResourceManager, sample_resources: list[Resource]
    ) -> None:
        """Test filtering resources by category."""
        for resource in sample_resources:
            resource_manager.add_resource(resource)

        ai_ml_resources = resource_manager.get_by_category(ResourceCategory.AI_ML)
        web_resources = resource_manager.get_by_category(ResourceCategory.WEB_DEV)

        assert len(ai_ml_resources) == 1
        assert len(web_resources) == 1
        assert ai_ml_resources[0].title == "PyTorch Tutorial"

    def test_get_by_difficulty(
        self, resource_manager: ResourceManager, sample_resources: list[Resource]
    ) -> None:
        """Test filtering resources by difficulty."""
        for resource in sample_resources:
            resource_manager.add_resource(resource)

        beginner = resource_manager.get_by_difficulty(DifficultyLevel.BEGINNER)
        intermediate = resource_manager.get_by_difficulty(DifficultyLevel.INTERMEDIATE)
        advanced = resource_manager.get_by_difficulty(DifficultyLevel.ADVANCED)

        assert len(beginner) == 1
        assert len(intermediate) == 1
        assert len(advanced) == 1

    def test_search_by_tag(
        self, resource_manager: ResourceManager, sample_resources: list[Resource]
    ) -> None:
        """Test searching resources by tag."""
        for resource in sample_resources:
            resource_manager.add_resource(resource)

        pytorch_resources = resource_manager.search_by_tag("pytorch")
        react_resources = resource_manager.search_by_tag("react")

        assert len(pytorch_resources) == 1
        assert len(react_resources) == 1
        assert pytorch_resources[0].title == "PyTorch Tutorial"

    def test_get_free_resources(
        self, resource_manager: ResourceManager, sample_resources: list[Resource]
    ) -> None:
        """Test filtering free resources."""
        for resource in sample_resources:
            resource_manager.add_resource(resource)

        # Add a paid resource
        paid_resource = Resource(
            title="Paid Course",
            url="https://example.com/paid",
            category=ResourceCategory.WEB_DEV,
            difficulty=DifficultyLevel.ADVANCED,
            description="Premium content",
            is_free=False,
        )
        resource_manager.add_resource(paid_resource)

        free_resources = resource_manager.get_free_resources()

        assert len(free_resources) == 3
        assert all(r.is_free for r in free_resources)

    def test_export_to_json(
        self, resource_manager: ResourceManager, sample_resource: Resource, tmp_path: Path
    ) -> None:
        """Test exporting resources to JSON."""
        resource_manager.add_resource(sample_resource)

        json_file = tmp_path / "resources.json"
        resource_manager.export_to_json(json_file)

        assert json_file.exists()

        import json

        with json_file.open() as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["title"] == "Test Resource"
