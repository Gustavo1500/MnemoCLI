import time
import readchar
from .ui import console, clear_screen, header, Panel

class PalaceWalk:
    def __init__(self, loci_amount, mode="normal"):
        self.loci_amount = loci_amount
        self.mode = mode
        
        if mode == "even":
            self.current_loci = 2
            self.step = 2
        elif mode == "odd":
            self.current_loci = 1
            self.step = 2
        else: # normal
            self.current_loci = 1
            self.step = 1

    def run(self):
        clear_screen()
        header(f"Palace {self.mode.capitalize()} Walk", f"Stations 1 to {self.loci_amount}")
        
        self.start_timer = time.perf_counter()
        count = 0
                
        while self.current_loci <= self.loci_amount:
            console.print(f"Loci: [bold cyan]{self.current_loci:02d}[/] [dim](Press any key...)[/]", end="\r")
            
            key = readchar.readkey()
            if key in ['\x03', '\x1b']: 
                console.print("\n[red]Walk aborted.[/]")
                return

            self.current_loci += self.step
            count += 1

        self.report(count)

    def report(self, count):
        stop_timer = time.perf_counter()
        total_time = stop_timer - self.start_timer
        avg_time = total_time / count if count > 0 else 0

        if avg_time <= 1.0:
            rating = "[bold green]INCREDIBLE![/]"
        elif avg_time <= 2.0:
            rating = "[bold yellow]GOOD[/]"
        else:
            rating = "[bold red]COULD BE BETTER[/]"

        console.print("\n")
        console.print(Panel(
            f"Total Time: [cyan]{total_time:.2f}s[/]\n"
            f"Avg per Loci: [cyan]{avg_time:.2f}s[/]\n"
            f"Rating: {rating}",
            title="Walk Statistics",
            expand=False
        ))
        console.print("[dim]Press any key to continue...[/]")
        readchar.readkey()
