import json
import datetime
from pathlib import Path
from rich.table import Table
from .ui import console

DATA_DIR = Path.home() / ".mnemocli" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

STATS_FILE = DATA_DIR / "olympic_history.json"

def save_olympic_run(discipline, allocated_time, actual_time, correct, total):
    """Saves Olympic mode session stats to JSON."""
    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing history
    if STATS_FILE.exists():
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = {}
    else:
        history = {}

    # Determine Run Number
    run_number = len(history) + 1
    run_key = f"RUN_{run_number}"

    # Calculate Metrics
    accuracy = (correct / total) * 100 if total > 0 else 0
    time_per_item = actual_time / total if total > 0 else 0

    # Create the run data
    history[run_key] = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": discipline,
        "allocated_time_mins": allocated_time,
        "actual_memorization_time_secs": round(actual_time, 2),
        "time_per_item_secs": round(time_per_item, 2),
        "amount": total,
        "correct": correct,
        "accuracy_percent": round(accuracy, 2)
    }

    # Save to file
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

def show_history_table():
    """Reads history and prints a formatted table."""
    if not STATS_FILE.exists():
        console.print("[yellow]No Olympic history found yet.[/]")
        return

    with open(STATS_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)

    table = Table(title="🏆 Olympic Mode History", header_style="bold magenta", border_style="cyan")
    table.add_column("Run", justify="center")
    table.add_column("Date", justify="center")
    table.add_column("Mode", justify="center")
    table.add_column("Items", justify="center")
    table.add_column("Time/Item", justify="right")
    table.add_column("Accuracy", justify="right")

    # Show only the last 10 runs to keep it clean
    last_runs = list(history.items())[-10:]

    for run_id, data in last_runs:
        acc = data['accuracy_percent']
        # Color code accuracy
        acc_str = f"[green]{acc}%[/]" if acc >= 90 else f"[yellow]{acc}%[/]" if acc >= 70 else f"[red]{acc}%[/]"
        
        table.add_row(
            run_id.replace("RUN_", "#"),
            data['date'].split(" ")[0], # Just the date
            data['mode'].capitalize(),
            str(data['amount']),
            f"{data['time_per_item_secs']}s",
            acc_str
        )

    console.print(table)
