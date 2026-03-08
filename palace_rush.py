import time
import readchar
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

class PalaceRush:
    def __init__(self, loci_amount, time_per_loci=2, reverse=False):
        self.time_per_loci = time_per_loci
        self.loci_amount = loci_amount
        self.reverse = reverse
        self.current_loci = loci_amount if reverse else 1
        self.time_log = {}
        self.console = Console()

    def run(self):
        self.console.print(Panel(f"[bold cyan]Palace Rush Started[/bold cyan]\nLoci: {self.loci_amount} | Target: {self.time_per_loci}s", expand=False))
        
        try:
            while True:
                if not self.reverse and self.current_loci > self.loci_amount:
                    break
                if self.reverse and self.current_loci < 1:
                    break

                self.process_loci()
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Session Interrupted.[/bold red]")
        
        if self.time_log:
            self.report()

    def process_loci(self):
        # Display current Loci
        print(f"\rLoci: {self.current_loci:02d} | Press any key...", end="", flush=True)
        
        start_time = time.perf_counter()
        key = readchar.readkey()
        
        if key in ['\x03', '\x1b']: # Ctrl+C or Esc
            raise KeyboardInterrupt

        total_time = time.perf_counter() - start_time
        self.time_log[self.current_loci] = total_time
        
        # Determine color for the live feedback
        ratio = total_time / self.time_per_loci
        color = "green" if ratio < 0.7 else "yellow" if ratio <= 1.1 else "red"
        
        self.console.print(f"\rLoci: {self.current_loci:02d} - [{color}]{total_time:.2f}s[/]        ")

        if not self.reverse:
            self.current_loci += 1
        else:
            self.current_loci -= 1

    def report(self):
        self.console.print("\n")
        self.console.print(Panel.fit("[bold white]PALACE RUSH PERFORMANCE REPORT[/]", border_style="magenta"))

        # 1. HEATMAP GRID
        heatmap_table = Table(title="Loci Heatmap", show_header=False, padding=(0, 1))
        for _ in range(5): # Create 5 columns
            heatmap_table.add_column()

        current_row = []
        sorted_loci_keys = sorted(self.time_log.keys())
        
        for loci in sorted_loci_keys:
            time_taken = self.time_log[loci]
            ratio = time_taken / self.time_per_loci

            if ratio < 0.7:
                style = "bold black on green"
            elif ratio <= 1.1:
                style = "bold black on yellow"
            else:
                style = "bold white on red"
            
            current_row.append(Text(f" {loci:02d} ", style=style))
            
            if len(current_row) == 5:
                heatmap_table.add_row(*current_row)
                current_row = []
        
        # Add remaining if not a perfect multiple of 5
        if current_row:
            while len(current_row) < 5:
                current_row.append("")
            heatmap_table.add_row(*current_row)

        self.console.print(heatmap_table)

        # 2. TOP 5 WORST LOCI (The "Bottlenecks")
        self.console.print("\n[bold red]Top 5 Bottlenecks (Slowest Loci):[/]")
        
        # Sort by time descending
        worst_loci = sorted(self.time_log.items(), key=lambda x: x[1], reverse=True)[:5]
        
        worst_table = Table(show_header=True, header_style="bold magenta")
        worst_table.add_column("Rank", justify="center")
        worst_table.add_column("Loci ID", justify="center")
        worst_table.add_column("Time", justify="right")
        worst_table.add_column("Vs Target", justify="right")

        for i, (loci, t) in enumerate(worst_loci, 1):
            diff = t - self.time_per_loci
            diff_str = f"+{diff:.2f}s" if diff > 0 else f"{diff:.2f}s"
            worst_table.add_row(
                str(i), 
                f"Loci {loci}", 
                f"{t:.2f}s", 
                f"[red]{diff_str}[/]" if diff > 0 else f"[green]{diff_str}[/]"
            )
        
        self.console.print(worst_table)

        # 3. SUMMARY
        avg_time = sum(self.time_log.values()) / len(self.time_log)
        self.console.print(f"\n[bold]Average Time:[/] {avg_time:.2f}s | [bold]Target:[/] {self.time_per_loci}s")
        self.console.print("-" * 30)

# Run the app
if __name__ == "__main__":
    run = PalaceRush(loci_amount=25, reverse=True)
    run.run()
