import random
import time
import math
import json
import readchar
from pathlib import Path
from mnemocli.ui import console, clear_screen, header
from rich.table import Table
from rich.panel import Panel

class RandomWords:
    def __init__(self, amount=100, total_time=5, language="portuguese"):
        self.amount: int = amount
        self.total_time: int = int(60 * total_time) 
        self.language: str = language
        self.random_words = []

        # 1. Load words from your specific folder
        master_words = self.read_json()
        if not master_words:
            console.print(f"[bold red]Failed to load words from languages/{self.language}.json. Exiting.[/]")
            return 
            
        self.amount = min(self.amount, len(master_words))

        # 2. Run the shuffle logic using your specific folder
        self.shuffle_logic(master_words)

    def read_json(self):
        MODULE_ROOT = Path(__file__).resolve().parent
        filepath = MODULE_ROOT / "languages" / f"{self.language}.json"
        
        if not filepath.exists():
            # If the file is missing, it creates "word_1" etc. 
            # Make sure your real file is actually at languages/portuguese.json
            self._create_dummy_json(filepath)

        try:
            with open(filepath, mode="r", encoding="utf-8") as f:
                data: dict = json.load(f)

            key = f"{self.language}_words"
            if key in data:
                return data[key]
            else:
                console.print(f"Invalid format in JSON. Expected key: '{key}'")
                return []
        except Exception as e:
            console.print(f"Error reading JSON: {e}")
            return []
            
    def _create_dummy_json(self, filepath: Path):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        dummy_words = [f"word_{i}" for i in range(1, 101)]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({f"{self.language}_words": dummy_words}, f, indent=4)

    def shuffle_logic(self, master_words):
        index_dir = Path.home() / ".mnemocli" / "data" / "shuffle_index"
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
            
            # If the dictionary size changed, reshuffle
            if len(state["words"]) != len(master_words):
                full_deck = master_words.copy()
                random.shuffle(full_deck)
                state = {"index": 0, "words": full_deck}

        current_index = state["index"]
        deck = state["words"]

        # If we need more words than are left in the deck, reshuffle and wrap around
        if current_index + self.amount > len(deck):
            remaining_words = deck[current_index:]
            needed_words = self.amount - len(remaining_words)

            new_deck = master_words.copy()
            random.shuffle(new_deck)

            # Prevent the last word of the old deck from being the first of the new deck
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
        clear_screen()
        header("Random Words", f"Memorize {len(self.random_words)} words")

        if not self.random_words:
            return
            
        ideal_cols = int(math.sqrt(len(self.random_words)))
        num_cols = max(3, (ideal_cols // 3) * 3) 
        
        table = Table(show_header=False, box=None, padding=(0, 2))
        for _ in range(num_cols):
            table.add_column(justify="center")

        for i in range(0, len(self.random_words), num_cols):
            chunk = self.random_words[i : i + num_cols]
            styled_row = [f"[bold cyan]{w}[/]" for w in chunk]
            if len(styled_row) < num_cols:
                styled_row.extend([""] * (num_cols - len(styled_row)))
            table.add_row(*styled_row)

        console.print(Panel(table, title="| Words to Memorize |", expand=False))
                
    def timer(self):
        console.print("\n[dim]Press [bold red]Ctrl+C[/] when you are ready to recall.[/dim]")
        start_timestamp = time.perf_counter()
        
        try:
            for i in range(self.total_time, -1, -1):
                mins, secs = divmod(i, 60)
                timer_str = f"{mins:02d}:{secs:02d}"
                print(f"\rTime remaining: {timer_str}   ", end="", flush=True)
                time.sleep(1)
        except KeyboardInterrupt:
            pass
            
        elapsed = time.perf_counter() - start_timestamp
        print("\r" + " " * 30 + "\r", end="", flush=True)
        time.sleep(0.2)
        
        return elapsed
    
    def user_input(self):
        user_answers = []
        ideal_cols = int(math.sqrt(len(self.random_words)))
        num_cols = max(3, (ideal_cols // 3) * 3)

        # 1. Input Loop
        for _ in range(len(self.random_words)):
            clear_screen()
            header("Recall Phase", f"Word {len(user_answers) + 1} of {len(self.random_words)}")
            
            table = Table(show_header=False, box=None, padding=(0, 2))
            for _ in range(num_cols):
                table.add_column(justify="center")

            for i in range(0, len(self.random_words), num_cols):
                row_data = []
                for j in range(i, i + num_cols):
                    if j < len(user_answers):
                        row_data.append(f"[bold cyan]{user_answers[j]}[/]")
                    elif j == len(user_answers):
                        row_data.append("[bold yellow underline]?[/]")
                    elif j < len(self.random_words):
                        row_data.append("[dim white].[/]")
                    else:
                        row_data.append("")
                table.add_row(*row_data)

            console.print(Panel(table, title="| Enter Words |", expand=False))
            
            try:
                val = input(f"\n > ").strip()
                user_answers.append(val)
            except KeyboardInterrupt:
                break 

        # 2. Final Report Screen
        clear_screen()
        header("Results", "Original vs Your Answers")
        
        orig_table = Table(show_header=False, box=None, padding=(0, 2))
        guess_table = Table(show_header=False, box=None, padding=(0, 2))
        
        for _ in range(num_cols):
            orig_table.add_column(justify="center")
            guess_table.add_column(justify="center")
            
        for i in range(0, len(self.random_words), num_cols):
            # Populate Original
            chunk = self.random_words[i : i + num_cols]
            styled_row = [f"[bold cyan]{w}[/]" for w in chunk]
            if len(styled_row) < num_cols:
                styled_row.extend([""] * (num_cols - len(styled_row)))
            orig_table.add_row(*styled_row)

            # Populate Guesses
            row_data = []
            for j in range(i, i + num_cols):
                if j < len(self.random_words):
                    orig_val = self.random_words[j].strip().lower()
                    
                    if j < len(user_answers):
                        guess_val = user_answers[j].strip().lower()
                        if orig_val == guess_val:
                            row_data.append(f"[bold green]{user_answers[j]}[/]")
                        else:
                            row_data.append(f"[bold red]{user_answers[j]}[/]")
                    else:
                        row_data.append("[dim]-[/]")
                else:
                    row_data.append("")
            guess_table.add_row(*row_data)

        console.print(Panel(orig_table, title="| Original Words |", expand=False))
        console.print(Panel(guess_table, title="| Your Guesses |", expand=False))

        correct = sum(1 for i, j in zip(self.random_words, user_answers) if i.strip().lower() == j.strip().lower())
        console.print(f"\n[bold]Done![/bold] Correct: [cyan]{correct}/{len(self.random_words)}[/cyan]\n")
        
        console.print("[dim]Press any key to return...[/]")
        readchar.readkey()
        
        return correct, len(self.random_words)
