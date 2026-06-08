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

        self.time_limit = 2 if set_time_limit else 0
        self.start_time = 0

        self.loci_shuffle = list(range(1, self.amount_loci + 1))
        random.shuffle(self.loci_shuffle)

        self.missed_loci = defaultdict(int)
        self.time_per_loci = defaultdict(list)
        self.number = None
        self.episode_count = 0

    def generate_number(self):
        if self.number is not None:
            self.evaluate()

        if not self.loci_shuffle:
            self.loci_shuffle = list(range(1, self.amount_loci + 1))
            random.shuffle(self.loci_shuffle)

        self.number = self.loci_shuffle.pop()
        self.start_time = time.perf_counter() 
        return self.number
    
    def evaluate(self):
        if self.start_time == 0:
            return
        
        actual_time = time.perf_counter() - self.start_time
        self.time_per_loci[self.number].append(actual_time)

        if self.time_limit > 0 and actual_time > self.time_limit:
            self.missed_loci[self.number] += 1

    def user_input(self):
        while True:
            try:
                key = readchar.readkey()
                if key in ['\x03', '\x1b']: 
                    return False
                if key:
                    self.episode_count += 1
                    return True
            except KeyboardInterrupt:
                return False

    def generate_report(self):
        self.evaluate()

        clear_screen()
        target_str = f"{self.time_limit}s" if self.time_limit > 0 else "None"
        header("Drill Heatmap Report", f"Target Time: {target_str}")
        
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

            current_row.append(Panel(f"[white]#{i:02d}[/]\n[{style}]{text}[/]", expand=True))

            if len(current_row) == 5:
                table.add_row(*current_row)
                current_row = []
        
        if current_row:
            while len(current_row) < 5:
                current_row.append("") 
            table.add_row(*current_row)
                
        console.print(table)
        
        if self.missed_loci:
            console.print("\n[bold red]Top Bottlenecks (Most Missed):[/]")
            sorted_missed = sorted(self.missed_loci.items(), key=lambda x: x[1], reverse=True)[:3]
            for loci, count in sorted_missed:
                console.print(f" • Loci {loci:02d}: [red]{count} times slow[/]")
        
        console.print("\n[dim]Press any key to exit report...[/]")
        try:
            readchar.readkey()
        except KeyboardInterrupt:
            pass
