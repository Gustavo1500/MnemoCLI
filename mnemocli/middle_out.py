import time
import readchar
from .ui import console, clear_screen, header, Panel

class MiddleOut:
    def __init__(self, loci_amount: int):
        self.loci_amount: int = loci_amount
        self.starting_point: int = int(self.loci_amount / 2)
        
        # We start at the middle. 
        # First half goes backwards from the middle-1 to 1.
        # Second half goes forwards from middle+1 to max.
        self.first_half = list(range(1, self.starting_point))
        self.second_half = list(range(self.starting_point + 1, self.loci_amount + 1))

        self.started = False
        self.toggle_fh = True # Alternation control
        self.start_timer = 0
        self.count = 0

    def calculate_loci(self):
        """Logic to alternate between first half and second half."""
        if not self.started:
            self.started = True
            return self.starting_point

        # If both are empty, we are done
        if not self.first_half and not self.second_half:
            return None

        # Determine which side to pull from
        # We use a toggle, but check if the list actually has items
        if self.toggle_fh and self.first_half:
            val = self.first_half.pop() # Takes the highest number left in the 1st half
            if self.second_half: # Only toggle if there's something to alternate to
                self.toggle_fh = False
            return val
        
        elif self.second_half:
            val = self.second_half.pop(0) # Takes the lowest number left in the 2nd half
            if self.first_half: # Only toggle if there's something to alternate to
                self.toggle_fh = True
            return val
            
        return None

    def run(self):
        clear_screen()
        header("Middle-Out Run", f"Starting at {self.starting_point}, expanding outwards")
        
        self.start_timer = time.perf_counter()
        
        while True:
            current_loci = self.calculate_loci()
            
            if current_loci is None:
                break

            console.print(f"Loci: [bold magenta]{current_loci:02d}[/] [dim](Press any key...)[/]", end="\r")
            
            if not self.user_input():
                console.print("\n[red]Run aborted.[/]")
                return

            self.count += 1

        self.report()

    def user_input(self) -> bool:
        """Capture keystroke to advance."""
        key = readchar.readkey()
        if key in ['\x03', '\x1b']: # Ctrl+C or Esc
            return False
        return True

    def report(self):
        stop_timer = time.perf_counter()
        total_time = stop_timer - self.start_timer
        avg_time = total_time / self.count if self.count > 0 else 0

        # Consistent rating system
        if avg_time <= 1.2:
            rating = "[bold green]ELITE SPEED[/]"
        elif avg_time <= 2.2:
            rating = "[bold yellow]STEADY FLOW[/]"
        else:
            rating = "[bold red]STUTTERED NAVIGATION[/]"

        console.print("\n")
        console.print(Panel(
            f"Total Time: [cyan]{total_time:.2f}s[/]\n"
            f"Avg per Loci: [cyan]{avg_time:.2f}s[/]\n"
            f"Loci Visited: [white]{self.count}[/]\n"
            f"Rating: {rating}",
            title="Middle-Out Statistics",
            expand=False,
            border_style="magenta"
        ))
        console.print("[dim]Press any key to continue...[/]")
        readchar.readkey()

if __name__ == "__main__":
    # For standalone testing
    md = MiddleOut(20)
    md.run()
