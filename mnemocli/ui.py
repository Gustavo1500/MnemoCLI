from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import readchar

# Single instance used by the whole app
console = Console()

def clear_screen():
    """Clears the terminal safely."""
    console.clear()

def header(title: str, subtitle: str = None):
    """Prints a standardized header for every mode."""
    content = Text()
    content.append(f"🏛️ {title.upper()} 🏛️\n", style="bold magenta")
    if subtitle:
        content.append(f"{subtitle}", style="dim white")
    
    console.print(Panel(content, expand=False, border_style="cyan"))

def press_to_continue(message: str = "Press any key to continue..."):
    """Standardized pause logic."""
    console.print(f"\n[dim]{message}[/]")
    try:
        readchar.readkey()
    except KeyboardInterrupt:
        pass

def select_option(options: list, title: str = "Select an option"):
    """
    Displays a list of options and waits for a single key press.
    Returns the index of the selected option or None if cancelled.
    """
    console.print(f"\n[bold cyan]{title}:[/]")
    for i, opt in enumerate(options, 1):
        console.print(f"  [bold yellow]{i}[/]. {opt}")
    
    console.print(f"\n[dim]Press number (1-{len(options)}) or Esc to cancel[/]")
    
    while True:
        try:
            key = readchar.readkey()
            if key == '\x1b' or key == '\x03': # Esc or Ctrl+C
                return None
            if key.isdigit():
                idx = int(key) - 1
                if 0 <= idx < len(options):
                    return idx
        except KeyboardInterrupt:
            return None
