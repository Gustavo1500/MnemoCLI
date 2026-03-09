import random
import time
import os
import math
from mnemocli.ui import console, clear_screen, header
from rich.table import Table
from rich.panel import Panel

class RandomNumbers:
    def __init__(self, amount=10, total_time=5):
        self.total_time = 60 * total_time # Convert minutes to seconds
        self.numbers = [random.randint(0, 9) for _ in range(amount)]

        self.console = console

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
            styled_row = [f"[bold cyan]{n}[/bold cyan]" for n in chunk]
            if len(styled_row) < num_cols:
                styled_row.extend([""] * (num_cols - len(styled_row)))
            table.add_row(*styled_row)

        self.console.print(
            Panel(table, title="| Numbers to Memorize | -> Horizontal -> |", expand=False)
        )
        self.timer()

    def timer(self):
        self.start_time = time.perf_counter()
        for i in range(self.total_time, -1, -1):
            mins, secs = divmod(i, 60)
            timer = f"{mins:02d}:{secs:02d}"
            print(f"\rTime remaining: {timer}", end="", flush=True)
            time.sleep(1)
        
        os.system("clear" if os.name == "posix" else "cls")
        self.user_input()  

    def user_input(self):
        user_answers = []
        ideal_cols = int(math.sqrt(len(self.numbers)))
        num_cols = max(3, (ideal_cols // 3) * 3)

        # 1. Input Loop
        for _ in range(len(self.numbers)):
            os.system("clear" if os.name == "posix" else "cls")
            
            table = Table(show_header=False, box=None, padding=(0, 2))
            for _ in range(num_cols):
                table.add_column(justify="center")

            for i in range(0, len(self.numbers), num_cols):
                row_data = []
                for j in range(i, i + num_cols):
                    if j < len(user_answers):
                        row_data.append(f"[bold cyan]{user_answers[j]}[/bold cyan]")
                    elif j == len(user_answers):
                        row_data.append("[bold white underline]?[/bold white underline]")
                    elif j < len(self.numbers):
                        row_data.append("[dim white].[/dim white]")
                    else:
                        row_data.append("")
                table.add_row(*row_data)

            self.console.print(Panel(table, title="| Enter Numbers |", expand=False))
            
            val = input(f" Slot {len(user_answers) + 1}: ")
            digit = int(val[0]) if val and val[0].isdigit() else 0
            user_answers.append(digit)

        # 2. Final Report Screen
        os.system("clear" if os.name == "posix" else "cls")
        
        # Build Original Table
        orig_table = Table(show_header=False, box=None, padding=(0, 2))
        for _ in range(num_cols):
            orig_table.add_column(justify="center")
            
        for i in range(0, len(self.numbers), num_cols):
            chunk = self.numbers[i : i + num_cols]
            styled_row = [f"[bold cyan]{n}[/bold cyan]" for n in chunk]
            if len(styled_row) < num_cols:
                styled_row.extend([""] * (num_cols - len(styled_row)))
            orig_table.add_row(*styled_row)

        # Build Guessed Table (Green = Correct, Red = Wrong)
        guess_table = Table(show_header=False, box=None, padding=(0, 2))
        for _ in range(num_cols):
            guess_table.add_column(justify="center")
            
        for i in range(0, len(self.numbers), num_cols):
            row_data = []
            for j in range(i, i + num_cols):
                if j < len(self.numbers):
                    orig_val = self.numbers[j]
                    guess_val = user_answers[j]
                    if orig_val == guess_val:
                        row_data.append(f"[bold green]{guess_val}[/bold green]")
                    else:
                        row_data.append(f"[bold red]{guess_val}[/bold red]")
                else:
                    row_data.append("")
            guess_table.add_row(*row_data)

        # Print the final comparison
        self.console.print(Panel(orig_table, title="| Original Numbers |", expand=False))
        self.console.print(Panel(guess_table, title="| Your Guesses |", expand=False))

        correct = sum(1 for i, j in zip(self.numbers, user_answers) if i == j)
        self.console.print(f"\n[bold]Done![/bold] Correct: [cyan]{correct}/{len(self.numbers)}[/cyan]\n")
