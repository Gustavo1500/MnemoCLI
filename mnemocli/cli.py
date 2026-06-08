import argparse
import sys
import time
import random
import readchar
import shutil
from pathlib import Path

from . import __version__

from .random_drill import RandomDrill
from .random_numbers import RandomNumbers
from .random_words import RandomWords
from .palace_rush import PalaceRush
from .palace_walk import PalaceWalk
from .middle_out import MiddleOut
from .ui import console, clear_screen, header, Panel

from .config_manager import load_config
from .stats_manager import save_olympic_run, show_history_table
from .graph_manager import interactive_graph

CONFIG = load_config()

def parse_args():
    parser = argparse.ArgumentParser(description="Memory Palace Training CLI")

    parser.add_argument("mode", choices=[
        "standard", "random_drill", "olympic", "palace_rush",
        "palace_rush_reverse", "random_numbers", "random_words",
        "even_run", "odd_run", "normal_run", "history", "graph",
        "middle_out", "info", "cleanup"
    ], help="The gamemode you want to play.")

    parser.add_argument("--loci_amount", "-la", type=int, 
                        help="Sets the amount of loci (Required for standard and palace-based modes).")
    
    parser.add_argument("--amount", "-a", type=int, 
                        help="Sets the amount of items (Required for random_numbers and random_words).")

    default_time = CONFIG.getint("Settings", "default_time", fallback=10)
    parser.add_argument("--time", "-t", type=int, default=default_time, 
                        help=f"Set time limit in minutes (Default from config: {default_time}).")

    args = parser.parse_args()

    palace_modes = ["standard", "random_drill", "palace_rush", "palace_rush_reverse", "even_run", "odd_run", "normal_run", "middle_out"]
    item_modes = ["random_numbers", "random_words"]

    if args.mode in palace_modes and args.loci_amount is None:
        parser.error(f"--loci_amount (-la) is required when playing the '{args.mode}' mode.")

    if args.mode in item_modes and args.amount is None:
        if args.loci_amount is not None:
            args.amount = args.loci_amount
        else:
            parser.error(f"--amount (-a) is required when playing the '{args.mode}' mode. Example: -a 20")

    return args


class Session:
    def __init__(self, loci_amount: int | None = None, item_amount: int | None = None, time_limit: int = 10):
        self.loci_amount = loci_amount
        self.item_amount = item_amount
        
        self.time_limit = time_limit 
        self.session_time_seconds = 60 * time_limit 

        self.language = CONFIG.get("Settings", "language", fallback="english").strip().lower()

        modes_str = CONFIG.get("StandardMode", "included_modes", fallback="random_drill, palace_rush, palace_rush_reverse, even_run, odd_run, middle_out")
        self.standard_modes = [m.strip() for m in modes_str.split(",") if m.strip()]

    def get_ready(self, mode_label):
        clear_screen()
        announcement = Panel(
            f"[bold yellow]PREPARE FOR:[/]\n[bold cyan]{mode_label.upper()}[/]",
            expand=False,
            border_style="yellow",
            padding=(1, 4)
        )
        console.print(announcement)
        console.print("\n")

        try:
            for i in range(3, 0, -1):
                console.print(f"[bold white]Starting in {i}...[/]")
                time.sleep(1)
                
            console.print("[bold green]GO![/]")
            time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("\n[red]Start interrupted.[/]")
            sys.exit(0)

    def run_single_mode(self, mode_name):
        friendly_names = {
            "normal_run": "Normal Palace Walk",
            "even_run": "Even Stations Walk",
            "odd_run": "Odd Stations Walk",
            "random_drill": "Random Station Drill",
            "palace_rush": "Palace Rush (Forward)",
            "palace_rush_reverse": "Palace Rush (Reverse)",
            "random_numbers": "Random Numbers",
            "random_words": "Random Words",
            "olympic": "Olympic Competition",
            "middle_out": "Middle-Out Expansion"
        }

        label = friendly_names.get(mode_name, "Next Challenge")

        if mode_name in ["even_run", "odd_run", "normal_run"]:
            self.get_ready(label)
            mode_type = mode_name.replace("_run", "")
            game = PalaceWalk(loci_amount=self.loci_amount, mode=mode_type)
            game.run()

        elif mode_name == "random_drill":
            self.get_ready(label)
            game = RandomDrill(self.loci_amount, standalone=True)
            clear_screen()
            header("Random Drill", "Visualize the station immediately")
            for i in range(self.loci_amount):
                num = game.generate_number()
                console.print(f"   [bold white]Progress: {i+1}/{self.loci_amount}[/] | [bold magenta]TARGET: {num:02d}[/]      ", end="\r")
                if not game.user_input():
                    console.print("\n[red]Drill aborted.[/]")
                    break
            game.generate_report()

        elif mode_name in ["palace_rush", "palace_rush_reverse"]:
            self.get_ready(label)
            is_reverse = "reverse" in mode_name
            game = PalaceRush(loci_amount=self.loci_amount, reverse=is_reverse)
            game.run()

        elif mode_name == "middle_out":
            self.get_ready(label)
            game = MiddleOut(loci_amount=self.loci_amount)
            game.run()

        elif mode_name == "random_numbers":
            self.get_ready(label)
            game = RandomNumbers(amount=self.item_amount, total_time=self.time_limit)
            game.show_numbers()
            game.timer()
            game.user_input()

        elif mode_name == "random_words":
            self.get_ready(label)
            game = RandomWords(amount=self.item_amount, total_time=self.time_limit, language=self.language)
            if game.random_words:
                game.show_words()
                game.timer()
                game.user_input()

        elif mode_name == "history":            
            clear_screen()
            show_history_table()
            console.print("\n[dim]Press any key to exit...[/]")
            try:
                readchar.readkey()
            except KeyboardInterrupt:
                pass

        elif mode_name == "graph":
            interactive_graph()

        elif mode_name == "info":
            import json
            
            data_path = Path.home() / ".mnemocli"
            config_path = data_path / "config.ini"
            stats_path = data_path / "data" / "olympic_history.json"

            header("System Dashboard", "Application State & Metrics")

            console.print(f"📦 [bold]Version:[/] {__version__}")
            console.print(f"👤 [bold]Author:[/] Gustavo1500")

            console.print(f"\n[bold underline]Active Configuration[/]")
            console.print(f"• [bold]Language:[/] {CONFIG.get('Settings', 'language', fallback='english').capitalize()}")
            console.print(f"• [bold]Default Session:[/] {CONFIG.getint('Settings', 'default_time', fallback=10)} minutes")
            
            run_count = 0
            if stats_path.exists():
                try:
                    with open(stats_path, "r", encoding="utf-8") as f:
                        run_count = len(json.load(f))
                except Exception:
                    run_count = "Error reading stats"

            console.print(f"\n[bold underline]Progress Statistics[/]")
            console.print(f"• [bold]Total Olympic Runs:[/] [green]{run_count}[/]")

            console.print(f"\n[bold underline]Environment[/]")
            console.print(f"• [bold]Config File:[/] [cyan]{config_path}[/]")
            
            if data_path.exists():
                try:
                    size = sum(f.stat().st_size for f in data_path.rglob('*') if f.is_file())
                    console.print(f"• [bold]Data Directory:[/] [cyan]{data_path}[/]")
                    console.print(f"• [bold]Disk Usage:[/] {size / 1024:.2f} KB")
                except Exception:
                    console.print("• [bold]Storage Used:[/] Unknown (Permission Error)")
            else:
                console.print("• [bold]Storage Used:[/] 0 KB (No data yet)")

            console.print(f"\n[dim]Tip: Use 'mnemocli cleanup' to wipe all history and reset settings.[/]")

        elif mode_name == "cleanup":
            data_path = Path.home() / ".mnemocli"
            
            if not data_path.exists() or not data_path.is_dir():
                console.print("[yellow]No data folder found to clean.[/]")
                return

            if data_path.name != ".mnemocli" or Path.home() not in data_path.parents:
                console.print("[bold red]CRITICAL SAFETY ERROR:[/] Path mismatch. Aborting.")
                return

            try:
                file_list = list(data_path.rglob("*"))
            except Exception as e:
                console.print(f"[bold red]Cannot access files:[/] {e}")
                return

            files = [f for f in file_list if f.is_file()]
            dirs = [d for d in file_list if d.is_dir()]

            MAX_FILES, MAX_DIRS = 100, 20
            if len(files) > MAX_FILES or len(dirs) > MAX_DIRS:
                console.print(f"[bold red]CIRCUIT BREAKER TRIGGERED![/]")
                console.print(f"Target contains too many items ({len(files)} files, {len(dirs)} dirs).")
                console.print("[red]Aborting. Please delete the folder manually for safety.[/]")
                return

            file_names = ", ".join([f"[cyan]{f.name}[/]" for f in files]) if files else "[dim]None[/]"
            dir_names = ", ".join([f"[blue]{d.name}[/]" for d in dirs]) if dirs else "[dim]None[/]"

            clear_screen()
            header("Data Cleanup", " < Erase Utility >")

            console.print(Panel(
                f"[bold red]CLEANUP: This action is permanent![/]\n\n"
                f"The following items will be deleted from [white underline]{data_path}[/]:\n\n"
                f"[bold white]Files to remove:[/] {file_names}\n"
                f"[bold white]Folders to remove:[/] {dir_names}\n\n"
                f"Total items: [bold yellow]{len(files) + len(dirs)}[/]",
                title="Review Deletion List",
                border_style="red",
                expand=False
            ))
            
            try:
                confirm = input("\nConfirm (type 'yes'): ").strip()
            except (KeyboardInterrupt, EOFError):
                console.print("\n[dim]Deletion aborted.[/]")
                return
            
            if confirm == "yes":
                try:
                    shutil.rmtree(data_path)
                    console.print("[bold green]✔ All data wiped. MnemoCLI is now fresh.[/]")
                except Exception as e:
                    console.print(f"[bold red]OS Error during deletion:[/] {e}")
            else:
                console.print("[dim]Confirmation did not match. Deletion aborted.[/]")

        elif mode_name == "olympic":
            clear_screen()
            header("Olympic Mode", "Standard memory competition events")
            
            console.print("Select your difficulty:\n")
            console.print("  1. [bold green]Beginner[/]     (50 items)")
            console.print("  2. [bold yellow]Intermediate[/] (100 items)")
            console.print("  3. [bold red]Advanced[/]     (200 items)")
            console.print("  4. [bold magenta]Pro[/]          (400 items)\n")
            
            while True:
                try:
                    console.print("[dim]Enter choice (1-4): [/]", end="")
                    choice = input().strip()
                    if choice in ["1", "2", "3", "4"]:
                        break
                    console.print("[red]Invalid choice. Please enter 1, 2, 3, or 4.[/]")
                except (KeyboardInterrupt, EOFError):
                    console.print("\n[red]Olympic mode aborted.[/]")
                    return
            
            settings = {
                "1": {"amount": 50, "time": 5},
                "2": {"amount": 100, "time": 5},
                "3": {"amount": 200, "time": 5},
                "4": {"amount": 400, "time": 5}
            }
            config = settings[choice]

            discipline = random.choice(["numbers", "words"])
            discipline_label = f"Olympic {discipline.capitalize()}"
            self.get_ready(discipline_label)

            actual_time = 0
            correct = 0
            total = 0

            if discipline == "numbers":
                game = RandomNumbers(amount=config["amount"], total_time=config["time"])
                game.show_numbers()
                actual_time = game.timer()
                correct, total = game.user_input()
            else:
                game = RandomWords(amount=config["amount"], total_time=config["time"], language=self.language)
                if game.random_words:
                    game.show_words()
                    actual_time = game.timer()
                    correct, total = game.user_input()

            if total > 0:
                save_olympic_run(
                    discipline=discipline,
                    allocated_time=config["time"],
                    actual_time=actual_time,
                    correct=correct,
                    total=total
                )
                console.print("\n[bold green]Stats Saved successfully to olympic_history.json![/]")
                time.sleep(1.5)

    def standard_mode(self):
        start_timer = time.perf_counter()

        self.run_single_mode("normal_run")

        base_modes = self.standard_modes.copy()
        if not base_modes:
            base_modes = ["random_drill"] 
            
        modes = base_modes.copy()
        random.shuffle(modes)

        while True:
            elapsed_time = time.perf_counter() - start_timer
            if elapsed_time >= self.session_time_seconds:
                console.print(f"\n[bold red]TIME'S UP![/] ({(elapsed_time / 60):.2f} mins elapsed)")
                break

            try:
                console.print("\n[dim]Continue to next drill? (y/n): [/]", end="")
                choice = readchar.readkey().strip().lower()
                console.print(choice) 
            except KeyboardInterrupt:
                break

            if choice == "n":
                break

            if not modes:
                modes = base_modes.copy()
                random.shuffle(modes)
            
            self.run_single_mode(modes.pop())

        self.report(start_timer)

    def report(self, start_timer):
        total_time = time.perf_counter() - start_timer
        mins, secs = divmod(int(total_time), 60)
        
        console.print("\n")
        console.print(Panel(
            f"[bold green]STANDARD SESSION COMPLETE[/]\n"
            f"Total Time Active: [cyan]{mins}m {secs}s[/]\n\n"
            "Great work sharpening your mind!",
            title="Summary",
            border_style="green",
            expand=False
        ))


def main():
    try:
        request = parse_args()
        
        session = Session(
            loci_amount=request.loci_amount,
            item_amount=request.amount, 
            time_limit=request.time
        )

        if request.mode == "standard":
            session.standard_mode()
        else:
            session.run_single_mode(request.mode)
            
    except KeyboardInterrupt:
        print("\n\nSession terminated by user. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
