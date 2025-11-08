"""Command-line interface for Software Development Lessons."""

import typer
from rich.console import Console
from rich.table import Table

from software_development_lessons import __version__
from software_development_lessons.core import LearningTracker, ResourceManager
from software_development_lessons.core.resource_manager import (
    DifficultyLevel,
    Resource,
    ResourceCategory,
)

app = typer.Typer(
    name="sdl",
    help="Software Development Lessons - Your ultimate learning companion!",
    add_completion=False,
)
console = Console()


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"[bold cyan]Software Development Lessons[/bold cyan] v{__version__}")


@app.command()
def add_resource(
    title: str = typer.Option(..., "--title", "-t", help="Resource title"),
    url: str = typer.Option(..., "--url", "-u", help="Resource URL"),
    category: str = typer.Option(..., "--category", "-c", help="Resource category"),
    difficulty: str = typer.Option(
        "beginner", "--difficulty", "-d", help="Difficulty level"
    ),
    description: str = typer.Option(
        "", "--description", "-desc", help="Resource description"
    ),
) -> None:
    """Add a new learning resource."""
    try:
        resource_category = ResourceCategory[category.upper()]
        difficulty_level = DifficultyLevel[difficulty.upper()]

        resource = Resource(
            title=title,
            url=url,
            category=resource_category,
            difficulty=difficulty_level,
            description=description,
        )

        manager = ResourceManager()
        manager.add_resource(resource)

        console.print(f"[green]✓[/green] Successfully added resource: [bold]{title}[/bold]")
    except (KeyError, ValueError) as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise typer.Exit(code=1) from e


@app.command()
def list_resources(
    category: str | None = typer.Option(None, "--category", "-c", help="Filter by category"),
) -> None:
    """List all learning resources."""
    manager = ResourceManager()

    # Add sample resources for demonstration
    _add_sample_resources(manager)

    resources = (
        manager.get_by_category(ResourceCategory[category.upper()])
        if category
        else manager.get_all()
    )

    if not resources:
        console.print("[yellow]No resources found.[/yellow]")
        return

    table = Table(title="Learning Resources", show_header=True, header_style="bold magenta")
    table.add_column("Title", style="cyan")
    table.add_column("Category", style="green")
    table.add_column("Difficulty", style="yellow")
    table.add_column("URL", style="blue")

    for resource in resources:
        table.add_row(
            resource.title,
            resource.category.value,
            resource.difficulty.value,
            resource.url,
        )

    console.print(table)


@app.command()
def stats() -> None:
    """Show learning statistics."""
    tracker = LearningTracker()

    # Add sample progress
    _add_sample_progress(tracker)

    statistics = tracker.get_statistics()

    table = Table(title="Learning Statistics", show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Resources", str(statistics["total_resources"]))
    table.add_row("Completed", str(statistics["completed"]))
    table.add_row("In Progress", str(statistics["in_progress"]))
    table.add_row("Average Completion", f"{statistics['average_completion']:.1f}%")
    table.add_row("Total Hours", f"{statistics['total_hours_spent']:.2f}h")

    console.print(table)


def _add_sample_resources(manager: ResourceManager) -> None:
    """Add sample resources for demonstration."""
    sample_resources = [
        Resource(
            title="PyTorch Tutorials",
            url="https://pytorch.org/tutorials/",
            category=ResourceCategory.AI_ML,
            difficulty=DifficultyLevel.INTERMEDIATE,
            description="Official PyTorch tutorials",
            tags=["deep-learning", "pytorch", "ai"],
        ),
        Resource(
            title="Next.js Documentation",
            url="https://nextjs.org/learn",
            category=ResourceCategory.WEB_DEV,
            difficulty=DifficultyLevel.BEGINNER,
            description="Learn Next.js framework",
            tags=["react", "nextjs", "web"],
        ),
        Resource(
            title="Kubernetes Tutorial",
            url="https://kubernetes.io/docs/tutorials/",
            category=ResourceCategory.CLOUD_DEVOPS,
            difficulty=DifficultyLevel.ADVANCED,
            description="Master container orchestration",
            tags=["kubernetes", "devops", "cloud"],
        ),
    ]

    for resource in sample_resources:
        try:
            manager.add_resource(resource)
        except ValueError:
            pass  # Resource already exists


def _add_sample_progress(tracker: LearningTracker) -> None:
    """Add sample progress for demonstration."""
    tracker.start_learning("https://pytorch.org/tutorials/")
    tracker.update_progress("https://pytorch.org/tutorials/", 75)

    tracker.start_learning("https://nextjs.org/learn")
    tracker.update_progress("https://nextjs.org/learn", 100)

    tracker.start_learning("https://kubernetes.io/docs/tutorials/")
    tracker.update_progress("https://kubernetes.io/docs/tutorials/", 30)


if __name__ == "__main__":
    app()
