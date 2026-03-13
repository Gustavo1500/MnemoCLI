import argparse
import sys
import time
import random
import readchar

# Import all the memory modes
from .random_drill import RandomDrill
from .random_numbers import RandomNumbers
from .random_words import RandomWords
from .palace_rush import PalaceRush
from .palace_walk import PalaceWalk
from .middle_out import MiddleOut
from .ui import console, clear_screen, header, Panel

# IMPORT THE CONFIG MANAGER
from .config_manager import load_config

# IMPORT STATS AND GRAPH MANAGERS
from .stats_manager import save_olympic_run
from .stats_manager import show_history_table
from .graph_manager import interactive_graph

# Load configuration globally
CONFIG = load_config()

def parse_args():
    parser = argparse.ArgumentParser(description="Memory Palace Training CLI")

    parser.add_argument("mode", choices=[
        "standard", "random_drill", "olympic", "palace_rush",
        "palace_rush_reverse", "random_numbers", "random_words",
        "even_run", "odd_run", "normal_run", "history", "graph",
        "middle_out"
    ], help="The gamemode you want to play.")

    parser.add_argument("--loci_amount", "-la", type=int, 
                        help="Sets the amount of loci (Required for standard and palace-based modes).")
    
    parser.add_argument("--amount", "-a", type=int, 
                        help="Sets the amount of items (Required for random_numbers and random_words).")

    # Read default time from config.ini
    default_time = CONFIG.getint("Settings", "default_time", fallback=10)
    parser.add_argument("--time", "-t", type=int, default=default_time, 
                        help=f"Set time limit in minutes (Default from config: {default_time}).")

    args = parser.parse_args()

    # --- VALIDATION LOGIC ---
    palace_modes = ["standard", "random_drill", "palace_rush", "palace_rush_reverse", "even_run", "odd_run", "normal_run"]
    item_modes = ["random_numbers", "random_words"]

    if args.mode in palace_modes and args.loci_amount is None:
        parser.error(f"--loci_amount (-la) is required when playing the '{args.mode}' mode.")

    if args.mode in item_modes and args.amount is None:
        if args.loci_amount is not None:
            args.amount = args.loci_amount
        else:
            parser.error(f"--amount (-a) is required when playing the '{args.mode}' mode.")

    return args


class Session:
    def __init__(self, loci_amount: int | None = None, item_amount: int | None = None, time_limit: int = 10):
        self.loci_amount = loci_amount
        self.item_amount = item_amount
        
        self.time_limit = time_limit 
        self.session_time_seconds = 60 * time_limit 

        # Pull Language from config
        self.language = CONFIG.get("Settings", "language", fallback="english").strip().lower()

        # Pull Standard Modes from config
        modes_str = CONFIG.get("StandardMode", "included_modes", fallback="random_drill, palace_rush")
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

        for i in range(3, 0, -1):
            console.print(f"[bold white]Starting in {i}...[/]")
            time.sleep(1)
            
        console.print("[bold green]GO![/]")
        time.sleep(0.5)

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
            "olympic": "Olympic Competition"
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
            self.get_ready("Middle-Out Expansion")
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
            readchar.readkey()

        elif mode_name == "graph":
            interactive_graph()

        elif mode_name == "olympic":
            clear_screen()
            header("Olympic Mode", "Standard memory competition events")
            
            console.print("Select your difficulty:\n")
            console.print("  1. [bold green]Beginner[/]     (50 items)")
            console.print("  2. [bold yellow]Intermediate[/] (100 items)")
            console.print("  3. [bold red]Advanced[/]     (200 items)")
            console.print("  4. [bold magenta]Pro[/]          (400 items)\n")
            
            while True:
                console.print("[dim]Enter choice (1-4): [/]", end="")
                choice = input().strip()
                if choice in ["1", "2", "3", "4"]:
                    break
                console.print("[red]Invalid choice. Please enter 1, 2, 3, or 4.[/]")
            
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

            # VARIABLES TO HOLD RESULTS
            actual_time = 0
            correct = 0
            total = 0

            # RUN THE SELECTED GAME AND CAPTURE DATA
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

            # SAVE THE OLYMPIC RUN TO HISTORY
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

        # USE THE MODES DEFINED IN config.ini
        base_modes = self.standard_modes.copy()
        
        # Fallback just in case user deleted all modes from config
        if not base_modes:
            base_modes = ["random_drill"] 
            
        modes = base_modes.copy()
        random.shuffle(modes)

        while True:
            elapsed_time = time.perf_counter() - start_timer
            if elapsed_time >= self.session_time_seconds:
                console.print(f"\n[bold red]TIME'S UP![/] ({(elapsed_time / 60):.2f} mins elapsed)")
                break

            console.print("\n[dim]Continue to next drill? (y/n): [/]", end="")
            choice = input().strip().lower()
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
