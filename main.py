import argparse
import sys
import time
import random

# Import all the memory modes
from mnemocli.random_drill import RandomDrill
from mnemocli.random_numbers import RandomNumbers
from mnemocli.random_words import RandomWords
from mnemocli.palace_rush import PalaceRush
from mnemocli.palace_walk import PalaceWalk
from mnemocli.ui import console, clear_screen, header, Panel


def parse_args():
    parser = argparse.ArgumentParser(description="Memory Palace Training CLI")

    # Added "normal_run" so it can be called standalone
    parser.add_argument("mode", choices=[
        "standard", "random_drill", "olympic", "palace_rush",
        "palace_rush_reverse", "random_numbers", "random_words",
        "even_run", "odd_run", "normal_run"
    ], help="The gamemode you want to play.")

    parser.add_argument("--loci_amount", "-la", type=int, 
                        help="Sets the amount of loci (Required for standard and palace-based modes).")
    
    parser.add_argument("--amount", "-a", type=int, 
                        help="Sets the amount of items (Required for random_numbers and random_words).")

    parser.add_argument("--time", "-t", type=int, default=10, 
                        help="Set time limit in minutes for the session/mode (Default: 10).")

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
    def __init__(self, loci_amount=None, item_amount=None, time_limit=10):
        self.loci_amount = loci_amount
        self.item_amount = item_amount
        
        self.time_limit = time_limit 
        self.session_time_seconds = 60 * time_limit 

        self.current_mode = None

    def get_ready(self, mode_label):
        clear_screen()
        
        # Create a big, obvious announcement of the mode
        announcement = Panel(
            f"[bold yellow]PREPARE FOR:[/]\n[bold cyan]{mode_label.upper()}[/]",
            expand=False,
            border_style="yellow",
            padding=(1, 4)
        )
        console.print(announcement)
        console.print("\n")

        # Countdown
        for i in range(3, 0, -1):
            console.print(f"[bold white]Starting in {i}...[/]")
            time.sleep(1)
            
        console.print("[bold green]GO![/]")
        time.sleep(0.5)

    def run_single_mode(self, mode_name):
        # Mapping slugs to friendly display names
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

        # 1. Palace Walk Modes
        if mode_name in ["even_run", "odd_run", "normal_run"]:
            self.get_ready(label) # Pass the friendly label
            mode_type = mode_name.replace("_run", "")
            game = PalaceWalk(loci_amount=self.loci_amount, mode=mode_type)
            game.run()

        # 2. Random Drill
        elif mode_name == "random_drill":
            self.get_ready(label)
            game = RandomDrill(self.loci_amount, standalone=True)
            clear_screen()
            header("Random Drill", "Visualize the station immediately")
            for i in range(self.loci_amount):
                num = game.generate_number()
                console.print(f"   [bold white]Progress: {i+1}/{self.loci_amount}[/] | [bold magenta]TARGET: {num:02d}[/]      ", end="\r")
                if not game.user_input():
                    break
            game.generate_report()

        # 3. Palace Rush
        elif mode_name in ["palace_rush", "palace_rush_reverse"]:
            self.get_ready(label)
            is_reverse = "reverse" in mode_name
            game = PalaceRush(loci_amount=self.loci_amount, reverse=is_reverse)
            game.run()

        # 4. Content Memorization
        elif mode_name == "random_numbers":
            self.get_ready(label)
            game = RandomNumbers(amount=self.item_amount, total_time=self.time_limit)
            game.show_numbers()

        # 5. Random Words
        elif mode_name == "random_words":
            self.get_ready(label)
            game = RandomWords(amount=self.item_amount, total_time=self.time_limit)
            if game.random_words:
                game.show_words()
                game.timer()
                game.user_input()

        # 6. Olympic Mode (Now using Rich UI)
        elif mode_name == "olympic":
            clear_screen()
            header("Olympic Mode", "Standard memory competition events (5 minutes limit)")
            
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

            # Randomly pick the competition discipline
            discipline = random.choice(["numbers", "words"])
            discipline_label = f"Olympic {discipline.capitalize()}"
            self.get_ready(discipline_label) # Inform user which discipline was picked

            if discipline == "numbers":
                game = RandomNumbers(amount=config["amount"], total_time=config["time"])
                game.show_numbers()
            else:
                game = RandomWords(amount=config["amount"], total_time=config["time"])
                if game.random_words:
                    game.show_words()
                    game.timer()
                    game.user_input()

    def standard_mode(self):
        start_timer = time.perf_counter()

        # 1. Start with a Normal Run
        self.run_single_mode("normal_run")

        # 2. Randomized Loop
        base_modes = ["random_drill", "palace_rush", "palace_rush_reverse", "even_run", "odd_run"]
        modes = base_modes.copy()
        random.shuffle(modes)

        while True:
            elapsed_time = time.perf_counter() - start_timer
            if elapsed_time >= self.session_time_seconds:
                console.print(f"\n[bold red]TIME'S UP![/] ({(elapsed_time / 60):.2f} mins elapsed)")
                break

            console.print("\n[dim]Continue to next random drill? (y/n): [/]", end="")
            choice = input().strip().lower()
            if choice == "n":
                break

            # FIX: Properly refill and shuffle the deck when empty
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


if __name__ == "__main__":
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
    