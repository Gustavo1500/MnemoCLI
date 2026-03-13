import json
import datetime
from pathlib import Path

STATS_FILE = Path("data/olympic_history.json")

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
