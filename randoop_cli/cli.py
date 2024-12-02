import click
from pathlib import Path
from .module_loader import load_module
from .class_inspection import get_classes
from .test_generator import randoop_test_generator, write_test_cases
import time
from rich.console import Console
from rich.progress import Progress

console = Console()

def simulate_loading(task_name, steps=5, delay=0.5):
    """Simulates a loading process with a progress bar."""
    with Progress(console=console) as progress:
        task = progress.add_task(f"[cyan]{task_name}...", total=steps)
        for _ in range(steps):
            time.sleep(delay)  # Simulating a delay
            progress.update(task, advance=1)

@click.command()
@click.option(
    "-k",
    "--sequence-length",
    type=int,
    default=2,
    help="Number of times to extend the sequence (default: 2)",
    show_default=True,
)
@click.option(
    "-f",
    "--file-paths",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    multiple=True,
    required=True,
    help="Paths to the Python files with class definitions",
)
def main(sequence_length, file_paths):
    """Python Randoop test generator for Python classes."""
    console.print("[bold blue]Randoop-Python Test Generator[/bold blue]\n")

    # Load all modules into a shared namespace
    shared_namespace = {}
    for file_path in file_paths:
        console.print(f"\n[bold yellow]Processing file: {file_path}[/bold yellow]\n")
        simulate_loading("Loading module")
        module = load_module(file_path, namespace=shared_namespace)

    # Inspect classes across all loaded modules
    simulate_loading("Inspecting classes")
    all_classes = []
    for name, obj in shared_namespace.items():
        if isinstance(obj, type):  # Ensure it's a class type
            all_classes.append((name, obj))

    if not all_classes:
        console.print("[bold red]No classes found in the provided files.[/bold red]")
        exit(1)

    # Generate tests
    simulate_loading("Generating Random tests")
    sequences, error_prone_cases, storage, instance_creation_data = randoop_test_generator(
        all_classes, sequence_length
    )

    # Write test cases
    write_test_cases(
        sequences=sequences,
        storage=storage,
        module_name="combined_namespace",
        file_path="combined_test_cases.py",
        instance_creation_data=instance_creation_data,
    )

    console.print("[bold green]All tasks completed successfully![/bold green]")



if __name__ == "__main__":
    main()
