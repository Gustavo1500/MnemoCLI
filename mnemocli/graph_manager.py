import json
from pathlib import Path
import plotext as plt
import readchar
from mnemocli.ui import console, clear_screen, header

# Absolute path resolution to prevent the "working directory" bug
BASE_DIR = Path(__file__).resolve().parent.parent
STATS_FILE = BASE_DIR / "data" / "olympic_history.json"

def interactive_graph():
    # 1. LOAD DATA
    if not STATS_FILE.exists():
        console.print("[yellow]No history found! Play some Olympic runs first.[/]")
        readchar.readkey()
        return

    with open(STATS_FILE, "r", encoding="utf-8") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            console.print("[red]History file is corrupted.[/]")
            readchar.readkey()
            return

    if not history:
        console.print("[yellow]History is empty.[/]")
        readchar.readkey()
        return

    # 2. EXTRACT DYNAMIC OPTIONS
    # Find all unique modes and amounts the user has actually played
    available_modes = sorted(list(set(r["mode"] for r in history.values())))
    available_amounts = sorted(list(set(r["amount"] for r in history.values())))

    metrics = {
        "1": ("accuracy_percent", "Accuracy (%)", "green"),
        "2": ("actual_memorization_time_secs", "Memorization Time (s)", "yellow"),
        "3": ("time_per_item_secs", "Time per Locus (s)", "cyan")
    }

    # Set default states
    current_metric_key = "1"
    current_mode = "all"
    current_amount = "all"

    # 3. INTERACTIVE LOOP
    while True:
        clear_screen()
        header("Performance Graph", "Interactive History Visualization")

        # Filter Data based on current state
        filtered_runs = []
        for run in history.values():
            if current_mode != "all" and run["mode"] != current_mode:
                continue
            if current_amount != "all" and run["amount"] != current_amount:
                continue
            filtered_runs.append(run)

        metric_field, metric_name, color = metrics[current_metric_key]

        # Draw the Plot
        plt.clear_figure()
        plt.theme("dark") # Fits the Rich dark terminal theme perfectly
        plt.plotsize(console.width or 80, 20)
        
        mode_label = current_mode.capitalize() if current_mode != "all" else "All Modes"
        amount_label = current_amount if current_amount != "all" else "All Amounts"
        plt.title(f"{metric_name} | {mode_label} | {amount_label}")

        if not filtered_runs:
            # Empty state for current filters
            console.print(f"\n[bold red]No data matches these filters.[/]\n")
        else:
            y_data = [r[metric_field] for r in filtered_runs]
            x_data = list(range(1, len(y_data) + 1)) # Sequential Run Index
            
            # Plot the data
            plt.plot(x_data, y_data, marker="dot", color=color)
            plt.ylabel(metric_name)
            plt.xlabel("Filtered Run Sequence")
            plt.show()

        # Render Controls Menu
        console.print("\n[bold cyan]--- Dashboard Controls ---[/]")
        console.print(f"[bold yellow]1-3[/]: Change Metric [dim](Current: {metric_name})[/]")
        console.print(f"[bold yellow]M[/]:   Toggle Mode   [dim](Current: {mode_label})[/]")
        console.print(f"[bold yellow]A[/]:   Toggle Amount [dim](Current: {amount_label})[/]")
        console.print(f"[bold red]Q[/]:   Quit to menu\n")

        # Listen for keystrokes
        key = readchar.readkey().lower()

        if key in ['q', '\x1b', '\x03']: # Q, Esc, or Ctrl+C
            break
        elif key in ['1', '2', '3']:
            current_metric_key = key
        elif key == 'm':
            # Cycle through modes dynamically
            modes_list = ["all"] + available_modes
            idx = modes_list.index(current_mode)
            current_mode = modes_list[(idx + 1) % len(modes_list)]
        elif key == 'a':
            # Cycle through amounts dynamically
            amounts_list = ["all"] + available_amounts
            idx = amounts_list.index(current_amount)
            current_amount = amounts_list[(idx + 1) % len(amounts_list)]
