import random
import time
import math
import readchar
from mnemocli.ui import console, clear_screen, header
from rich.table import Table
from rich.panel import Panel

class RandomNumbers:
    def __init__(self, amount=10, total_time=5):
        self.total_time = 60 * total_time # Convert minutes to seconds
        self.numbers = [random.randint(0, 9) for _ in range(amount)]

    def show_numbers(self):
        clear_screen()
        header("Random Numbers", f"Memorize {len(self.numbers)} digits")
        
        ideal_cols = int(math.sqrt(len(self.numbers)))
        num_cols = max(3, (ideal_cols // 3) * 3) 
        
        table = Table(show_header=False, box=None, padding=(0, 2))
        for _ in range(num_cols):
            table.add_column(justify="center")

        for i in range(0, len(self.numbers), num_cols):
            chunk = self.numbers[i : i + num_cols]
            styled_row = [f"[bold cyan]{n}[/]" for n in chunk]
            if len(styled_row) < num_cols:
                styled_row.extend([""] * (num_cols - len(styled_row)))
            table.add_row(*styled_row)

        console.print(Panel(table, title="| Numbers to Memorize | -> Horizontal -> |", expand=False))
        self.timer()

    def timer(self):
        console.print("\n[dim]Press [bold red]Ctrl+C[/] when you are ready to recall.[/dim]")
        self.start_time = time.perf_counter()
        
        try:
            for i in range(self.total_time, -1, -1):
                mins, secs = divmod(i, 60)
                timer_str = f"{mins:02d}:{secs:02d}"
                print(f"\rTime remaining: {timer_str}   ", end="", flush=True)
                time.sleep(1)
        except KeyboardInterrupt:
            # Safely catch Ctrl+C to skip timer
            pass
        finally:
            print("\r" + " " * 30 + "\r", end="", flush=True) 
            time.sleep(0.2) # Prevent double-taps from bubbling into the input loop
            self.user_input()

    def user_input(self):
        user_answers = []
        ideal_cols = int(math.sqrt(len(self.numbers)))
        num_cols = max(3, (ideal_cols // 3) * 3)

        # 1. Instant Input Loop
        while len(user_answers) < len(self.numbers):
            clear_screen()
            header("Recall Phase", "Type the numbers as fast as you can!")
            
            table = Table(show_header=False, box=None, padding=(0, 2))
            for _ in range(num_cols):
                table.add_column(justify="center")

            for i in range(0, len(self.numbers), num_cols):
                row_data = []
                for j in range(i, i + num_cols):
                    if j < len(user_answers):
                        row_data.append(f"[bold cyan]{user_answers[j]}[/]")
                    elif j == len(user_answers):
                        row_data.append("[bold yellow underline]?[/]")
                    elif j < len(self.numbers):
                        row_data.append("[dim white].[/]")
                    else:
                        row_data.append("")
                table.add_row(*row_data)

            console.print(Panel(table, title="| Enter Numbers |", expand=False))
            console.print(f"\n[dim]Slot {len(user_answers) + 1}/{len(self.numbers)}[/dim] (Press 'Backspace' to delete, 'Esc' to quit)")
            
            key = readchar.readkey()
            
            if key in ['\x03', '\x1b']: # Ctrl+C or Esc
                break
            elif key in ['\x08', '\x7f']: # Backspace
                if user_answers:
                    user_answers.pop()
            elif key.isdigit():
                user_answers.append(int(key))

        # 2. Final Report Screen
        clear_screen()
        header("Results", "Original vs Your Answers")
        
        orig_table = Table(show_header=False, box=None, padding=(0, 2))
        guess_table = Table(show_header=False, box=None, padding=(0, 2))
        
        for _ in range(num_cols):
            orig_table.add_column(justify="center")
            guess_table.add_column(justify="center")
            
        for i in range(0, len(self.numbers), num_cols):
            # Populate Original
            chunk = self.numbers[i : i + num_cols]
            styled_row = [f"[bold cyan]{n}[/]" for n in chunk]
            if len(styled_row) < num_cols:
                styled_row.extend([""] * (num_cols - len(styled_row)))
            orig_table.add_row(*styled_row)

            # Populate Guesses
            row_data = []
            for j in range(i, i + num_cols):
                if j < len(self.numbers):
                    orig_val = self.numbers[j]
                    
                    if j < len(user_answers):
                        guess_val = user_answers[j]
                        if orig_val == guess_val:
                            row_data.append(f"[bold green]{guess_val}[/]")
                        else:
                            row_data.append(f"[bold red]{guess_val}[/]")
                    else:
                        row_data.append("[dim]-[/]") # Mark un-entered as blank
                else:
                    row_data.append("")
            guess_table.add_row(*row_data)

        console.print(Panel(orig_table, title="| Original Numbers |", expand=False))
        console.print(Panel(guess_table, title="| Your Guesses |", expand=False))

        correct = sum(1 for i, j in zip(self.numbers, user_answers) if i == j)
        console.print(f"\n[bold]Done![/bold] Correct: [cyan]{correct}/{len(self.numbers)}[/cyan]\n")
        
        console.print("[dim]Press any key to return...[/]")
        readchar.readkey()
