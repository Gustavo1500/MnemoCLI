import argparse
import sys
import time
import random

# Import all the memory modes
from random_drill import RandomDrill
from random_numbers import RandomNumbers
from random_words import RandomWords
from palace_rush import PalaceRush
from pairrun import PairRun
from normal_run import NormalRun


def parse_args():
    parser = argparse.ArgumentParser(description="Memory Palace Training CLI")

    parser.add_argument("mode", choices=[
        "standard", "random_drill", "olympic", "palace_rush",
        "palace_rush_reverse", "random_numbers", "random_words",
        "even_run", "odd_run"
    ], help="The gamemode you want to play.")

    parser.add_argument("--loci_amount", "-la", type=int, 
                        help="Sets the amount of loci (Required for standard and palace-based modes).")
    
    parser.add_argument("--amount", "-a", type=int, 
                        help="Sets the amount of items (Required for random_numbers and random_words).")

    # Set session time (defaults to 10 min)
    parser.add_argument("--time", "-t", type=int, default=10, 
                        help="Set time limit in minutes for the session/mode (Default: 10).")

    args = parser.parse_args()

    # --- VALIDATION LOGIC ---
    palace_modes = ["standard", "random_drill", "palace_rush", "palace_rush_reverse", "even_run", "odd_run"]
    item_modes = ["random_numbers", "random_words"]

    # 1. Palace modes require --loci_amount
    if args.mode in palace_modes and args.loci_amount is None:
        parser.error(f"--loci_amount (-la) is required when playing the '{args.mode}' mode.")

    # 2. Item modes require --amount
    if args.mode in item_modes and args.amount is None:
        # Fallback: if the user mistakenly used -la instead of -a, accept it anyway
        if args.loci_amount is not None:
            args.amount = args.loci_amount
        else:
            parser.error(f"--amount (-a) is required when playing the '{args.mode}' mode.")

    # 3. Olympic requires neither (it uses fixed internal amounts based on difficulty)

    return args


class Session:
    def __init__(self, loci_amount=None, item_amount=None, time_limit=10):
        self.loci_amount = loci_amount
        self.item_amount = item_amount
        
        self.time_limit = time_limit # Kept in minutes for random_words/numbers
        self.session_time_seconds = 60 * time_limit # Converted to seconds for standard mode loop

        self.current_mode = None

    def get_ready(self):
        print("Get ready!")
        t = 3
        for _ in range(3):
            time.sleep(1)
            print(t)
            t -= 1

        time.sleep(0.5)
        print("GO!")
        time.sleep(0.5)

    def run_single_mode(self, mode_name):
        """A dispatcher that handles the execution of any given mode."""
        
        if mode_name == "random_drill":
            game = RandomDrill(self.loci_amount, standalone=True)
            self.current_mode = game
            print("\n ~ RANDOM DRILL ~")
            self.get_ready()

            # Drill the user exactly the amount of loci they have
            for _ in range(self.loci_amount):
                game.generate_number()
                print(f"\nLOCI: {game.number}")
                game.user_input()

            game.generate_report()

        elif mode_name == "random_numbers":
            game = RandomNumbers(amount=self.item_amount, total_time=self.time_limit)
            self.current_mode = game
            print("\n ~ RANDOM NUMBERS ~")
            self.get_ready()
            game.show_numbers()

        elif mode_name == "random_words":
            game = RandomWords(amount=self.item_amount, total_time=self.time_limit)
            self.current_mode = game
            print("\n ~ RANDOM WORDS ~")
            self.get_ready()
            
            if game.random_words: 
                game.show_words()
                game.timer()
                game.user_input()

        elif mode_name == "palace_rush":
            game = PalaceRush(loci_amount=self.loci_amount)
            self.current_mode = game
            print("\n ~ PALACE RUSH ~")
            self.get_ready()
            game.run()
            
        elif mode_name == "palace_rush_reverse":
            game = PalaceRush(loci_amount=self.loci_amount, reverse=True)
            self.current_mode = game
            print("\n ~ PALACE RUSH (REVERSE) ~")
            self.get_ready()
            game.run()

        elif mode_name in ["even_run", "odd_run"]:
            mode_type = "even" if mode_name == "even_run" else "odd"
            game = PairRun(loci_amount=self.loci_amount, mode=mode_type)
            self.current_mode = game
            print(f"\n ~ {mode_type.upper()} RUN ~")
            self.get_ready()
            game.run()

        elif mode_name == "olympic":
            print("\n" + "="*40)
            print("           OLYMPIC MODE")
            print("="*40)
            print("Standard memory competition events (5 minutes limit).")
            print("Select your difficulty:")
            print("1. Beginner     (50 items)")
            print("2. Intermediate (100 items)")
            print("3. Advanced     (200 items)")
            print("4. Pro          (400 items)")
            
            while True:
                choice = input("Enter choice (1-4): ").strip()
                if choice in ["1", "2", "3", "4"]:
                    break
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
            
            # Standard 5 minute competition formats
            settings = {
                "1": {"amount": 50, "time": 5},
                "2": {"amount": 100, "time": 5},
                "3": {"amount": 200, "time": 5},
                "4": {"amount": 400, "time": 5}
            }
            config = settings[choice]

            # Randomly pick the competition discipline
            discipline = random.choice(["numbers", "words"])
            self.get_ready()

            if discipline == "numbers":
                print(f"\n ~ SPEED NUMBERS ({config['amount']} digits, {config['time']} mins) ~")
                game = RandomNumbers(amount=config["amount"], total_time=config["time"])
                self.current_mode = game
                game.show_numbers() 
            
            elif discipline == "words":
                print(f"\n ~ RANDOM WORDS ({config['amount']} words, {config['time']} mins) ~")
                game = RandomWords(amount=config["amount"], total_time=config["time"])
                self.current_mode = game
                if game.random_words:
                    game.show_words()
                    game.timer()
                    game.user_input()

    def standard_mode(self):
        start_timer = time.perf_counter()

        # 1. NORMAL RUN
        print("\n ~ NORMAL RUN ~")
        game = NormalRun(self.loci_amount)
        self.get_ready()
        game.run()

        # 2. RANDOMIZED LOOP
        modes = ["random_drill", "palace_rush", "palace_rush_reverse", "even_run", "odd_run"]

        while True:
            # Check total elapsed time BEFORE starting the next round
            elapsed_time = time.perf_counter() - start_timer
            
            if elapsed_time >= self.session_time_seconds:
                print("\n" + "="*40)
                print(f" TIME'S UP! ({(elapsed_time / 60):.2f} minutes elapsed)")
                print("="*40)
                break

            user_input = input("\nContinue to next random drill? (y/n): ").strip().lower()

            if user_input == "n":
                break
            
            # Select and run a random mode
            random_selection = random.choice(modes)
            self.run_single_mode(random_selection)

        self.report(start_timer)
        
    def report(self, start_timer):
        # Final goodbye/report when exiting standard mode
        total_time = time.perf_counter() - start_timer
        mins, secs = divmod(int(total_time), 60)
        
        print("\n" + "="*40)
        print("         STANDARD SESSION COMPLETE")
        print("="*40)
        print(f"Total Time Active: {mins}m {secs}s")
        print("Good Game!")
        print("="*40 + "\n")


if __name__ == "__main__":
    try:
        request = parse_args()
        
        # Instantiate the session using the safely parsed arguments
        session = Session(
            loci_amount=request.loci_amount,
            item_amount=request.amount, 
            time_limit=request.time
        )

        if request.mode == "standard":
            # Launch the mixed loop
            session.standard_mode()
        else:
            # Launch whatever standalone mode was requested
            session.run_single_mode(request.mode)
            
    except KeyboardInterrupt:
        print("\n\nSession terminated by user. Goodbye!")
        sys.exit(0)
