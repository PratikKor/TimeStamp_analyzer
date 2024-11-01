import os
import threading
import csv
import json
from datetime import datetime
from queue import Queue
from rich import print
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.prompt import Prompt, IntPrompt, Confirm
import pandas as pd  # For exporting to Excel

# Initialize console for Rich output
console = Console()
file_queue = Queue()
results = []

# Configuration settings
class Config:
    num_threads = 4
    recursive = True
    follow_symlinks = False  # Option to follow symbolic links
    sort_by = "created"  # Options: created, modified, accessed
    filter_extension = None
    min_size = 0  # Minimum file size in bytes
    max_size = float('inf')  # Maximum file size in bytes
    date_range = (None, None)  # Tuple to filter by date range (start, end)
    export_format = "csv"  # Options: csv, json, excel
    output_file = "timestamps_output"

# Analyze timestamps and collect details for each file
def analyze_timestamps(file_path):
    try:
        # Fetch file timestamps and other details
        creation_time = os.path.getctime(file_path)
        modification_time = os.path.getmtime(file_path)
        access_time = os.path.getatime(file_path)
        file_size = os.path.getsize(file_path)

        # Date range filtering
        if Config.date_range[0] and creation_time < Config.date_range[0]:
            return
        if Config.date_range[1] and creation_time > Config.date_range[1]:
            return

        # Convert to human-readable format
        creation_time_str = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        modification_time_str = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
        access_time_str = datetime.fromtimestamp(access_time).strftime('%Y-%m-%d %H:%M:%S')

        # Append to results
        results.append({
            "file": file_path,
            "size": file_size,
            "created": creation_time_str,
            "modified": modification_time_str,
            "accessed": access_time_str
        })
    
    except Exception as e:
        console.print(f"[red]Error analyzing {file_path}: {e}[/red]")

# Worker function for threaded file analysis
def worker(progress, task_id):
    while not file_queue.empty():
        file_path = file_queue.get()
        analyze_timestamps(file_path)
        progress.update(task_id, advance=1)
        file_queue.task_done()

# Main function to configure and start the analyzer
def main():
    # Allow users to enter any directory path, even outside the script's location
    directory = Prompt.ask("Enter the absolute or relative path to the directory to scan for timestamps")
    directory = os.path.abspath(directory)  # Convert to absolute path for clarity
    if not os.path.exists(directory):
        console.print(f"[red]Error: The specified directory does not exist.[/red]")
        return

    Config.num_threads = IntPrompt.ask("Enter the number of threads to use", default=Config.num_threads)
    Config.recursive = Confirm.ask("Scan recursively?", default=True)
    Config.follow_symlinks = Confirm.ask("Follow symbolic links?", default=False)
    Config.filter_extension = Prompt.ask("Filter by file extension (e.g., .txt, .jpg)", default="")
    Config.min_size = IntPrompt.ask("Minimum file size in bytes", default=0)
    Config.max_size = IntPrompt.ask("Maximum file size in bytes", default=float('inf'))
    Config.sort_by = Prompt.ask("Sort files by (created, modified, accessed)", default=Config.sort_by)
    Config.export_format = Prompt.ask("Export format (csv, json, excel)", default=Config.export_format)

    # Populate file queue based on filters
    for root, dirs, files in os.walk(directory, followlinks=Config.follow_symlinks):
        if not Config.recursive:
            dirs.clear()  # Stop recursive scan if chosen
        for file in files:
            file_path = os.path.join(root, file)
            if Config.filter_extension and not file.endswith(Config.filter_extension):
                continue
            if Config.min_size <= os.path.getsize(file_path) <= Config.max_size:
                file_queue.put(file_path)

    # Initialize and start worker threads with progress bar
    with Progress() as progress:
        task_id = progress.add_task("[green]Analyzing files...", total=file_queue.qsize())
        threads = [threading.Thread(target=worker, args=(progress, task_id)) for _ in range(Config.num_threads)]
        for thread in threads:
            thread.start()
        file_queue.join()
        for thread in threads:
            thread.join()

    # Sort and display results
    results.sort(key=lambda x: x[Config.sort_by])
    display_results()

    # Export results if requested
    if Config.export_format in ["csv", "json", "excel"]:
        export_results()

# Display results in a table
def display_results():
    table = Table(title="Timestamp Analysis Results")
    table.add_column("File", style="cyan", overflow="fold")
    table.add_column("Size (Bytes)", style="blue")
    table.add_column("Created", style="green")
    table.add_column("Modified", style="yellow")
    table.add_column("Accessed", style="magenta")

    for result in results:
        table.add_row(result["file"], str(result["size"]), result["created"], result["modified"], result["accessed"])

    console.print(table)
    console.print(f"[bold cyan]Total files analyzed:[/bold cyan] {len(results)}")

# Export results to the selected format
def export_results():
    filename = f"{Config.output_file}.{Config.export_format}"
    if Config.export_format == "csv":
        with open(filename, mode="w", newline='') as csv_file:
            fieldnames = ["file", "size", "created", "modified", "accessed"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    elif Config.export_format == "json":
        with open(filename, mode="w") as json_file:
            json.dump(results, json_file, indent=4)
    elif Config.export_format == "excel":
        df = pd.DataFrame(results)
        df.to_excel(f"{filename}.xlsx", index=False)

    console.print(f"[green]Results exported to {filename}[/green]")

if __name__ == "__main__":
    main()
