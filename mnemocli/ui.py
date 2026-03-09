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
    readchar.readkey()
