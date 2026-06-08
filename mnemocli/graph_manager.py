import json
from pathlib import Path
import plotext as plt
import readchar
from .ui import console, clear_screen, header

DATA_DIR = Path.home() / ".mnemocli" / "data"
STATS_FILE = DATA_DIR / "olympic_history.json"

def interactive_graph():
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

    sorted_history = sorted(
        history.values(), 
        key=lambda x: x.get("date", "")
    )

    available_modes = sorted(list(set(r.get("mode", "unknown") for r in sorted_history)))
    available_amounts = sorted(list(set(r.get("amount", 0) for r in sorted_history)))

    metrics = {
        "1": ("accuracy_percent", "Accuracy (%)", "green"),
        "2": ("actual_memorization_time_secs", "Memorization Time (s)", "yellow"),
        "3": ("time_per_item_secs", "Time per Locus (s)", "cyan")
    }

    current_metric_key = "1"
    current_mode = "all"
    current_amount = "all"

    while True:
        clear_screen()
        header("Performance Graph", "Interactive History Visualization")

        filtered_runs = []
        for run in sorted_history:
            if current_mode != "all" and run.get("mode") != current_mode:
                continue
            if current_amount != "all" and run.get("amount") != current_amount:
                continue
            filtered_runs.append(run)

        metric_field, metric_name, color = metrics[current_metric_key]

        plt.clear_figure()
        plt.theme("dark")
        term_width = console.width if console.width and console.width > 20 else 80
        plt.plotsize(term_width, 20)
        
        mode_label = str(current_mode).capitalize() if current_mode != "all" else "All Modes"
        amount_label = str(current_amount) if current_amount != "all" else "All Amounts"
        plt.title(f"{metric_name} | {mode_label} | {amount_label}")

        if not filtered_runs:
            console.print(f"\n[bold red]No data matches these filters.[/]\n")
        else:
            y_data = [r.get(metric_field, 0) for r in filtered_runs]
            x_data = list(range(1, len(y_data) + 1))
            
            plt.plot(x_data, y_data, marker="dot", color=color)
            plt.ylabel(metric_name)
            plt.xlabel("Filtered Run Sequence")
            plt.show()

        console.print("\n[bold cyan]--- Dashboard Controls ---[/]")
        console.print(f"[bold yellow]1-3[/]: Change Metric [dim](Current: {metric_name})[/]")
        console.print(f"[bold yellow]M[/]:   Toggle Mode   [dim](Current: {mode_label})[/]")
        console.print(f"[bold yellow]A[/]:   Toggle Amount [dim](Current: {amount_label})[/]")
        console.print(f"[bold red]Q[/]:   Quit to menu\n")

        try:
            key = readchar.readkey().lower()
        except KeyboardInterrupt:
            break

        if key in ['q', '\x1b', '\x03']: 
            break
        elif key in ['1', '2', '3']:
            current_metric_key = key
        elif key == 'm':
            modes_list = ["all"] + available_modes
            idx = modes_list.index(current_mode)
            current_mode = modes_list[(idx + 1) % len(modes_list)]
        elif key == 'a':
            amounts_list = ["all"] + available_amounts
            idx = amounts_list.index(current_amount)
            current_amount = amounts_list[(idx + 1) % len(amounts_list)]
