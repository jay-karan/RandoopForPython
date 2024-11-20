import click
from pathlib import Path
from .module_loader import load_module
from .class_inspection import get_classes
from .test_generator import randoop_test_generator, write_regression_tests
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
    "--file-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    required=True,
    help="Path to the Python file with class definitions",
)
def main(sequence_length, file_path):
    """Python Randoop test generator for Python classes."""
    console.print("[bold blue]Randoop-Python Test Generator[/bold blue]\n")

    # Simulate loading for module loading
    simulate_loading("Loading module")
    module = load_module(file_path)

    # Simulate loading for class inspection
    simulate_loading("Inspecting classes")
    classes = get_classes(module)

    if not classes:
        console.print(f"[bold red]No classes found in '{file_path}'.[/bold red]")
        exit(1)

    # Simulate loading for test generation
    simulate_loading("Generating Random tests")
    sequences, error_prone_cases, storage = randoop_test_generator(classes, sequence_length)

    # Display Successful Sequences
    console.print("\n[bold green]Successful Sequences:[/bold green]")
    for sequence in sequences:
        for cls_name, method_name, args, result in sequence:
            console.print(f"[green]{cls_name}.{method_name}({args}) -> {result}[/green]")

    # Display Error-Prone Sequences
    console.print("\n[bold yellow]Error-Prone Sequences:[/bold yellow]")
    for each_error_prone_case in error_prone_cases:
        for cls_name, method_name, args, error in each_error_prone_case:
            console.print(f"[yellow]{cls_name}.{method_name}({args}) -> Error: {error}[/yellow]")

    # Simulate loading for writing regression tests
    simulate_loading("Writing regression tests")
    write_regression_tests(sequences, module.__name__, file_path)

    console.print("[bold green]All tasks completed successfully![/bold green]")

if __name__ == "__main__":
    main()
