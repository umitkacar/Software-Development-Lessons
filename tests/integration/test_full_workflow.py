"""Integration tests for the full learning workflow."""

from pathlib import Path

import pytest

from software_development_lessons.core import LearningTracker, ResourceManager
from software_development_lessons.core.resource_manager import (
    DifficultyLevel,
    Resource,
    ResourceCategory,
)


@pytest.mark.integration
class TestFullLearningWorkflow:
    """Integration tests for the complete learning workflow."""

    def test_complete_learning_journey(
        self, resource_manager: ResourceManager, learning_tracker: LearningTracker
    ) -> None:
        """Test a complete learning journey from discovery to completion."""
        # Step 1: Add resources to the manager
        pytorch_resource = Resource(
            title="PyTorch Fundamentals",
            url="https://pytorch.org/tutorials/beginner/basics/intro.html",
            category=ResourceCategory.AI_ML,
            difficulty=DifficultyLevel.BEGINNER,
            description="Learn PyTorch basics",
            tags=["pytorch", "deep-learning", "fundamentals"],
        )
        resource_manager.add_resource(pytorch_resource)

        # Step 2: Find resources by category
        ai_ml_resources = resource_manager.get_by_category(ResourceCategory.AI_ML)
        assert len(ai_ml_resources) == 1

        # Step 3: Start learning the resource
        selected_resource = ai_ml_resources[0]
        session1 = learning_tracker.start_learning(selected_resource.url)
        assert session1.resource_url == selected_resource.url

        # Step 4: Make some progress
        learning_tracker.update_progress(selected_resource.url, 25)
        progress = learning_tracker.get_progress(selected_resource.url)
        assert progress is not None
        assert progress.completion_percentage == 25

        # Step 5: Complete first session
        session1.complete(notes="Completed intro module")

        # Step 6: Continue learning in another session
        _session2 = learning_tracker.start_learning(selected_resource.url)
        learning_tracker.update_progress(selected_resource.url, 100)

        # Step 7: Verify completion
        progress = learning_tracker.get_progress(selected_resource.url)
        assert progress is not None
        assert progress.completion_percentage == 100
        assert progress.completed_at is not None

        # Step 8: Check statistics
        stats = learning_tracker.get_statistics()
        assert stats["total_resources"] == 1
        assert stats["completed"] == 1
        assert stats["in_progress"] == 0

    def test_multiple_resources_workflow(
        self, resource_manager: ResourceManager, learning_tracker: LearningTracker
    ) -> None:
        """Test learning multiple resources simultaneously."""
        # Add multiple resources
        resources = [
            Resource(
                title="React Basics",
                url="https://react.dev/learn",
                category=ResourceCategory.WEB_DEV,
                difficulty=DifficultyLevel.BEGINNER,
                description="Learn React fundamentals",
                tags=["react", "javascript"],
            ),
            Resource(
                title="Docker Tutorial",
                url="https://docs.docker.com/get-started/",
                category=ResourceCategory.CLOUD_DEVOPS,
                difficulty=DifficultyLevel.INTERMEDIATE,
                description="Container fundamentals",
                tags=["docker", "containers"],
            ),
        ]

        for resource in resources:
            resource_manager.add_resource(resource)

        # Start learning both resources
        for resource in resources:
            learning_tracker.start_learning(resource.url)

        # Make different progress on each
        learning_tracker.update_progress(resources[0].url, 100)  # Complete React
        learning_tracker.update_progress(resources[1].url, 50)  # Half Docker

        # Verify progress
        completed = learning_tracker.get_completed_resources()
        in_progress = learning_tracker.get_in_progress_resources()

        assert len(completed) == 1
        assert len(in_progress) == 1
        assert completed[0].resource_url == resources[0].url
        assert in_progress[0].resource_url == resources[1].url

    def test_resource_filtering_and_selection(self, resource_manager: ResourceManager) -> None:
        """Test filtering resources by multiple criteria."""
        # Add diverse resources
        resources = [
            Resource(
                title="Advanced PyTorch",
                url="https://pytorch.org/tutorials/advanced/",
                category=ResourceCategory.AI_ML,
                difficulty=DifficultyLevel.ADVANCED,
                description="Advanced PyTorch techniques",
                tags=["pytorch", "advanced"],
            ),
            Resource(
                title="Beginner PyTorch",
                url="https://pytorch.org/tutorials/beginner/",
                category=ResourceCategory.AI_ML,
                difficulty=DifficultyLevel.BEGINNER,
                description="PyTorch for beginners",
                tags=["pytorch", "beginner"],
            ),
            Resource(
                title="Next.js Guide",
                url="https://nextjs.org/learn",
                category=ResourceCategory.WEB_DEV,
                difficulty=DifficultyLevel.BEGINNER,
                description="Next.js tutorial",
                tags=["nextjs", "react"],
            ),
        ]

        for resource in resources:
            resource_manager.add_resource(resource)

        # Filter by category
        ai_ml = resource_manager.get_by_category(ResourceCategory.AI_ML)
        assert len(ai_ml) == 2

        # Filter by difficulty
        beginner = resource_manager.get_by_difficulty(DifficultyLevel.BEGINNER)
        assert len(beginner) == 2

        # Search by tag
        pytorch = resource_manager.search_by_tag("pytorch")
        assert len(pytorch) == 2

    def test_export_and_statistics(
        self,
        resource_manager: ResourceManager,
        learning_tracker: LearningTracker,
        tmp_path: Path,
    ) -> None:
        """Test exporting resources and generating statistics."""
        # Add and track resources
        resource = Resource(
            title="Kubernetes Deep Dive",
            url="https://kubernetes.io/docs/tutorials/kubernetes-basics/",
            category=ResourceCategory.CLOUD_DEVOPS,
            difficulty=DifficultyLevel.ADVANCED,
            description="Master Kubernetes",
            tags=["kubernetes", "devops"],
        )
        resource_manager.add_resource(resource)

        # Export resources
        export_path = tmp_path / "resources.json"
        resource_manager.export_to_json(export_path)
        assert export_path.exists()

        # Track learning
        learning_tracker.start_learning(resource.url)
        learning_tracker.update_progress(resource.url, 75)

        # Get statistics
        stats = learning_tracker.get_statistics()
        assert stats["total_resources"] == 1
        assert stats["average_completion"] == 75.0
        assert stats["in_progress"] == 1
