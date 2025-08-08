# screen_tui/cli.py
import sys
from .core import start_session
from rich.console import Console

console = Console()

def help():
    console.print("""
[bold green]screen_tui[/bold green] - terminal screen-session handler.

Usage:
  screen_tui              Launch interactive UI
  screen_tui -h|--help    Show help
  screen_tui -j NAME JOB  Create session (non-interactive)

License: MIT, inspired by Perl version by Jiri Nemecek
""")
    sys.exit(0)

def main():
    if len(sys.argv) == 1:
        import curses
        from .ui import main_menu
        curses.wrapper(main_menu)
    elif sys.argv[1] in ['-h', '--help']:
        help()
    elif sys.argv[1] == '-j':
        if len(sys.argv) < 3:
            console.print("[red]Error:[/red] Missing session name.")
            sys.exit(1)
        name = sys.argv[2].replace(' ', '_')
        job = sys.argv[3] if len(sys.argv) > 3 else ''
        code, msg = start_session(name, job)
        if code:
            console.print(f"[red]Failed:[/red] {msg}")
            sys.exit(code)
        console.print(f"[green]Session '{name}' created.[/green]")
    else:
        console.print(f"[red]Unknown argument(s):[/red] {' '.join(sys.argv[1:])}")
        help()
