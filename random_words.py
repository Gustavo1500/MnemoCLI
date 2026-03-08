import random
import time
import os
import math
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class RandomWords:
    def __init__(self, amount=100, total_time=5, language="portuguese"):
        self.amount: int = amount
        # FIX: Cast to integer to prevent TypeError if user passes a float (e.g., 0.5 mins)
        self.total_time: int = int(60 * total_time) 
        self.language: str = language
        self.console = Console()
        self.random_words = []

        # Load master words
        master_words = self.read_json()
        if not master_words:
            self.console.print("[bold red]Failed to load words. Exiting.[/bold red]")
            return 
            
        # Ensure we don't ask for more words than exist in total dictionary
        self.amount = min(self.amount, len(master_words))

        # Run the shuffle logic
        self.shuffle_logic(master_words)

    def read_json(self):
        filepath = Path(f"json/{self.language}.json")
        
        # FIX: Auto-generate dummy JSON for testing if it doesn't exist
        if not filepath.exists():
            self._create_dummy_json(filepath)

        try:
            with open(filepath, mode="r", encoding="utf-8") as f:
                data: dict = json.load(f)

            key = f"{self.language}_words"
            if key in data:
                return data[key]
            else:
                print(f"Invalid format in JSON. Expected key: '{key}'")
                return []
                
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return []
            
    def _create_dummy_json(self, filepath: Path):
        """Helper to create a sample file so the code runs out of the box."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        dummy_words = [f"word_{i}" for i in range(1, 51)] # 50 dummy words
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({f"{self.language}_words": dummy_words}, f, indent=4)
        print(f"Created dummy file at {filepath}")

    def shuffle_logic(self, master_words):
        index_dir = Path("json/shuffle_index")
        index_dir.mkdir(parents=True, exist_ok=True) 
        index_shuffle = index_dir / f"shuffle_index_{self.language}.json"

        master_words = sorted(set(master_words))
        state = {}

        if not index_shuffle.exists():
            full_deck = master_words.copy()
            random.shuffle(full_deck)
            state = {"index": 0, "words": full_deck}
        else:
            with open(index_shuffle, mode="r", encoding="utf-8") as f:
                state = json.load(f)
            
            if len(state["words"]) != len(master_words):
                full_deck = master_words.copy()
                random.shuffle(full_deck)
                state = {"index": 0, "words": full_deck}

        current_index = state["index"]
        deck = state["words"]

        if current_index + self.amount > len(deck):
            remaining_words = deck[current_index:]
            needed_words = self.amount - len(remaining_words)

            new_deck = master_words.copy()
            random.shuffle(new_deck)

            if remaining_words and new_deck[0] == remaining_words[-1]:
                new_deck[0], new_deck[-1] = new_deck[-1], new_deck[0]

            self.random_words = remaining_words + new_deck[:needed_words]
            state["words"] = new_deck
            state["index"] = needed_words
        else:
            self.random_words = deck[current_index : current_index + self.amount]
            state["index"] = current_index + self.amount

        with open(index_shuffle, mode="w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=4)

    def show_words(self):
        if not self.random_words:
            return
            
        ideal_cols = int(math.sqrt(len(self.random_words)))
        num_cols = max(3, (ideal_cols // 3) * 3) 
        
        table = Table(show_header=False, box=None, padding=(0, 2))
        for _ in range(num_cols):
            table.add_column(justify="center")

        for i in range(0, len(self.random_words), num_cols):
            chunk = self.random_words[i : i + num_cols]
            styled_row = [f"[bold cyan]{w}[/bold cyan]" for w in chunk]
            if len(styled_row) < num_cols:
                styled_row.extend([""] * (num_cols - len(styled_row)))
            table.add_row(*styled_row)

        self.console.print(
            Panel(table, title="| Words to Memorize | -> Horizontal -> |", expand=False)
        )
        
        # FIX: Removed self.timer() from here. Methods should do one thing.
        
    def timer(self):
        for i in range(self.total_time, -1, -1):
            mins, secs = divmod(i, 60)
            timer_str = f"{mins:02d}:{secs:02d}"
            print(f"\rTime remaining: {timer_str}", end="", flush=True)
            time.sleep(1)
        
        # FIX: Removed self.user_input() from here. 

    def user_input(self):
        os.system("clear" if os.name == "posix" else "cls")
        user_answers = []
        ideal_cols = int(math.sqrt(len(self.random_words)))
        num_cols = max(3, (ideal_cols // 3) * 3)

        # 1. Input Loop
        for _ in range(len(self.random_words)):
            os.system("clear" if os.name == "posix" else "cls")
            
            table = Table(show_header=False, box=None, padding=(0, 2))
            for _ in range(num_cols):
                table.add_column(justify="center")

            for i in range(0, len(self.random_words), num_cols):
                row_data = []
                for j in range(i, i + num_cols):
                    if j < len(user_answers):
                        row_data.append(f"[bold cyan]{user_answers[j]}[/bold cyan]")
                    elif j == len(user_answers):
                        row_data.append("[bold white underline]?[/bold white underline]")
                    elif j < len(self.random_words):
                        row_data.append("[dim white].[/dim white]")
                    else:
                        row_data.append("")
                table.add_row(*row_data)

            self.console.print(Panel(table, title="| Enter Words |", expand=False))
            
            val = input(f" Word {len(user_answers) + 1}: ").strip()
            user_answers.append(val)

        # 2. Final Report Screen
        os.system("clear" if os.name == "posix" else "cls")
        
        orig_table = Table(show_header=False, box=None, padding=(0, 2))
        guess_table = Table(show_header=False, box=None, padding=(0, 2))
        
        for _ in range(num_cols):
            orig_table.add_column(justify="center")
            guess_table.add_column(justify="center")
            
        for i in range(0, len(self.random_words), num_cols):
            chunk = self.random_words[i : i + num_cols]
            styled_row = [f"[bold cyan]{w}[/bold cyan]" for w in chunk]
            if len(styled_row) < num_cols:
                styled_row.extend([""] * (num_cols - len(styled_row)))
            orig_table.add_row(*styled_row)

            row_data = []
            for j in range(i, i + num_cols):
                if j < len(self.random_words):
                    orig_val = self.random_words[j]
                    guess_val = user_answers[j]
                    
                    if orig_val.lower() == guess_val.lower():
                        row_data.append(f"[bold green]{guess_val}[/bold green]")
                    else:
                        row_data.append(f"[bold red]{guess_val}[/bold red]")
                else:
                    row_data.append("")
            guess_table.add_row(*row_data)

        self.console.print(Panel(orig_table, title="| Original Words |", expand=False))
        self.console.print(Panel(guess_table, title="| Your Guesses |", expand=False))

        correct = sum(1 for i, j in zip(self.random_words, user_answers) if i.lower() == j.lower())
        self.console.print(f"\n[bold]Done![/bold] Correct: [cyan]{correct}/{len(self.random_words)}[/cyan]\n")

if __name__ == "__main__":
    # Note: 0 total_time results in exactly 00:00, sleeping for 1 second, then proceeding.
    rw = RandomWords(amount=10, total_time=0) 
    
    if rw.random_words: # Only run if words successfully loaded
        rw.show_words()
        rw.timer()
        rw.user_input()
