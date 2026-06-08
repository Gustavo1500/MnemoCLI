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
    
    if STATS_FILE.exists():
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = {}
    else:
        history = {}

    run_number = len(history) + 1
    run_key = f"RUN_{run_number}"

    accuracy = (correct / total) * 100 if total > 0 else 0
    time_per_item = actual_time / total if total > 0 else 0

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

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

def show_history_table():
    """Reads history and prints a formatted table."""
    if not STATS_FILE.exists():
        console.print("[yellow]No Olympic history found yet.[/]")
        return

    with open(STATS_FILE, "r", encoding="utf-8") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            console.print("[red]History file is corrupted.[/]")
            return

    table = Table(title="🏆 Olympic Mode History", header_style="bold magenta", border_style="cyan")
    table.add_column("Run", justify="center")
    table.add_column("Date", justify="center")
    table.add_column("Mode", justify="center")
    table.add_column("Items", justify="center")
    table.add_column("Time/Item", justify="right")
    table.add_column("Accuracy", justify="right")

    sorted_history = sorted(
        history.items(), 
        key=lambda x: int(x[0].split('_')[1]) if '_' in x[0] else 0
    )
    last_runs = sorted_history[-15:]

    for run_id, data in last_runs:
        acc = data.get('accuracy_percent', 0)
        acc_str = f"[green]{acc}%[/]" if acc >= 90 else f"[yellow]{acc}%[/]" if acc >= 70 else f"[red]{acc}%[/]"
        
        table.add_row(
            run_id.replace("RUN_", "#"),
            data.get('date', 'Unknown').split(" ")[0],
            data.get('mode', 'Unknown').capitalize(),
            str(data.get('amount', 0)),
            f"{data.get('time_per_item_secs', 0)}s",
            acc_str
        )

    console.print(table)
