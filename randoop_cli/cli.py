import click
from pathlib import Path
import requests
import zipfile
import os
import shutil
from io import BytesIO
from .module_loader import load_module
from .class_inspection import get_classes
from .test_generator import randoop_test_generator, write_regression_tests
import time
from rich.console import Console
from rich.progress import Progress
import time

console = Console()

def simulate_loading(task_name, steps=5, delay=0.5):
    """Simulates a loading process with a progress bar."""
    with Progress(console=console) as progress:
        task = progress.add_task(f"[cyan]{task_name}...", total=steps)
        for _ in range(steps):
            time.sleep(delay)  # Simulating a delay
            progress.update(task, advance=1)

def download_and_extract_repo(repo_url, temp_dir):
    """
    Downloads a GitHub repository as a zip file and extracts it to a temporary directory.
    """
    if not repo_url.endswith(".git"):
        repo_url = repo_url.rstrip("/") + ".git"
    
    zip_url = repo_url.replace(".git", "/archive/refs/heads/master.zip")
    console.print(f"Downloading repository from: {zip_url}")
    
    response = requests.get(zip_url, stream=True)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as zf:
            zf.extractall(temp_dir)
    else:
        console.print(f"[bold red]Failed to download the repository: {response.status_code}[/bold red]")
        exit(1)

def identify_source_files(repo_path):
    """
    Identifies source code files in the repository by excluding non-code files like docs, tests, and examples.
    """
    source_files = []
    for root, dirs, files in os.walk(repo_path):
        # Ignore non-source directories
        ignored_dirs = {"docs", "examples", "tests", ".github", "__pycache__"}
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        for file in files:
            if file.endswith(".py") and not file.startswith("__init__"):
                source_files.append(Path(root) / file)
    
    return source_files

import re
from collections import defaultdict, deque

def parse_imports(file_path):
    """
    Parse a Python file to extract imported modules or files.
    """
    imports = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"^\s*(?:from|import) (\S+)", line)
            if match:
                imports.append(match.group(1).split('.')[0])  # Extract the module name
    return imports

def resolve_dependencies(source_files):
    """
    Resolve file loading order based on import dependencies using topological sorting.
    """
    dependency_graph = defaultdict(set)
    file_map = {file.stem: file for file in source_files}

    # Build the dependency graph
    for file in source_files:
        imports = parse_imports(file)
        for module in imports:
            if module in file_map:  # Only consider local modules
                dependency_graph[file.stem].add(module)

    # Perform topological sorting
    visited = set()
    resolved = []
    temp_stack = set()

    def visit(node):
        if node in temp_stack:
            raise ValueError(f"Circular dependency detected: {node}")
        if node not in visited:
            temp_stack.add(node)
            for dep in dependency_graph[node]:
                visit(dep)
            temp_stack.remove(node)
            visited.add(node)
            resolved.append(node)

    for file in source_files:
        if file.stem not in visited:
            visit(file.stem)

    # Return files in the resolved order
    return [file_map[stem] for stem in resolved]

@click.command()
@click.option(
    "-k",
    "--sequence-length",
    type=int,
    default=10,
    help="Number of times to extend the sequence (default: 2)",
    show_default=True,
)
@click.option(
    "--repo-url",
    type=str,
    default=None,
    help="GitHub repository URL to process.",
)
@click.option(
    "-f",
    "--file",
    "file_paths",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    multiple=True,
    help="Path to individual Python files to process (use -f multiple times for multiple files).",
)
def main(sequence_length, repo_url, file_paths):
    """
    Process a GitHub repository URL or multiple Python source files and generate test cases for their classes.
    """
    console.print("[bold blue]Randoop-Python Test Generator[/bold blue]\n")

    # Temporary directory for repository
    temp_dir = Path("temp_repo")

    try:
        shared_namespace = {}

        if repo_url:
            # If a GitHub repository URL is provided, process the repository
            console.print("[bold green]Processing GitHub repository...[/bold green]")
            simulate_loading("Downloading repository")
            download_and_extract_repo(repo_url, temp_dir)

            # Identify source files in the repository
            repo_root = next(temp_dir.iterdir())  # First directory inside the extracted repo
            simulate_loading("Identifying source files")
            source_files = identify_source_files(repo_root)
        elif file_paths:
            # If files are provided via -f, process them
            console.print("[bold green]Processing provided files...[/bold green]")
            source_files = list(file_paths)
        else:
            console.print("[bold red]No repository URL or files provided. Please specify one.[/bold red]")
            exit(1)

        # Resolve dependencies and sort files
        source_files = resolve_dependencies(source_files)

        # Load all source files into the shared namespace
        for file_path in source_files:
            console.print(f"\n[bold yellow]Processing file: {file_path}[/bold yellow]\n")
            simulate_loading("Loading module")
            load_module(file_path, shared_namespace)

        # Inspect classes
        simulate_loading("Inspecting classes")
        all_classes = [
            (name, obj)
            for name, obj in shared_namespace.items()
            if isinstance(obj, type)  # Only consider class types
        ]
        if not all_classes:
            console.print("[bold red]No classes found in the source files.[/bold red]")
            exit(1)

        # Generate tests
        simulate_loading("Generating Random tests")
        sequences, error_prone_cases, storage, instance_creation_data = randoop_test_generator(
            all_classes, sequence_length
        )

        # Display Successful Sequences
        console.print("\n[bold green]-----> Generated Instances and Sequences:[/bold green]")
        for seq in sequences:
            print(seq)

        # Display Error-Prone Test Cases
        console.print("\n[bold yellow]-----> Error-Prone Test Cases:[/bold yellow]")
        for error in error_prone_cases:
            print(error)


        # Write test cases
        write_test_cases(
            sequences=sequences,
            storage=storage,
            module_name="combined_namespace",
            file_path="combined_test_cases.py",
            instance_creation_data=instance_creation_data,
        )

        console.print("[bold green]All tasks completed successfully![/bold green]")

    finally:
        # Cleanup temporary directory if used
        if repo_url and temp_dir.exists():
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main()
