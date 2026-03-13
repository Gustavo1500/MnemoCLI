import random
import time
import readchar
from collections import defaultdict
from .ui import console, header, clear_screen
from rich.table import Table
from rich.panel import Panel

class RandomDrill:
    def __init__(self, amount_loci, set_time_limit=True, standalone=False):
        self.amount_loci = amount_loci
        self.standalone = standalone

        # Time variables
        self.time_limit = 2 if set_time_limit else 0
        self.start_time = 0

        # Fisher-Yates Shuffle Initialization
        self.loci_shuffle = list(range(1, self.amount_loci + 1))
        random.shuffle(self.loci_shuffle)

        # Logging
        self.missed_loci = defaultdict(int)
        self.time_per_loci = defaultdict(list)
        self.number = None
        self.episode_count = 0

    def generate_number(self):
        # If this isn't the first run, evaluate the PREVIOUS number
        if self.number is not None:
            self.evaluate()

        # Refill shuffle deck if empty
        if not self.loci_shuffle:
            self.loci_shuffle = list(range(1, self.amount_loci + 1))
            random.shuffle(self.loci_shuffle)

        self.number = self.loci_shuffle.pop()
        self.start_time = time.perf_counter() # Start timing NOW
        return self.number
    
    def evaluate(self):
        """Calculates time taken for the CURRENT self.number"""
        if self.start_time == 0:
            return
        
        actual_time = time.perf_counter() - self.start_time
        self.time_per_loci[self.number].append(actual_time)

        if self.time_limit > 0 and actual_time > self.time_limit:
            self.missed_loci[self.number] += 1

    def user_input(self):
        """Wait for user acknowledgment without creating a new line."""
        while True:
            key = readchar.readkey()
            
            # Handle exit keys
            if key in ['\x03', '\x1b']: # Ctrl+C or Esc
                return False
            
            # Any other key counts as a "hit"
            if key:
                self.episode_count += 1
                return True

    def generate_report(self):
        # IMPORTANT: Evaluate the very last number before showing the report
        self.evaluate()

        clear_screen()
        header("Drill Heatmap Report", f"Target Time: {self.time_limit}s")
        
        table = Table(show_header=False, padding=(0, 1), box=None, show_edge=False)
        for _ in range(5): 
            table.add_column(justify="center")

        current_row = []
        for i in range(1, self.amount_loci + 1):
            times = self.time_per_loci.get(i)
            
            if not times:
                style, text = "dim white", "--"
            else:
                avg = sum(times) / len(times)
                text = f"{avg:.1f}s"
                ratio = avg / self.time_limit if self.time_limit > 0 else 0
                style = "bold green" if ratio < 0.8 else "bold yellow" if ratio <= 1.2 else "bold red"

            # Create a stylized tile
            current_row.append(Panel(f"[white]#{i:02d}[/]\n[{style}]{text}[/]", expand=True))

            if len(current_row) == 5:
                table.add_row(*current_row)
                current_row = []
        
        # FIX: Handle the "Leftover Row" if loci_amount is not a multiple of 5
        if current_row:
            while len(current_row) < 5:
                current_row.append("") # Fill empty spots
            table.add_row(*current_row)
                
        console.print(table)
        
        # Optional: Print top bottlenecks
        if self.missed_loci:
            console.print("\n[bold red]Top Bottlenecks (Most Missed):[/]")
            sorted_missed = sorted(self.missed_loci.items(), key=lambda x: x[1], reverse=True)[:3]
            for loci, count in sorted_missed:
                console.print(f" • Loci {loci:02d}: [red]{count} times slow[/]")
        
        console.print("\n[dim]Press any key to exit report...[/]")
        readchar.readkey()
