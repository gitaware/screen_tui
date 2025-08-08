# screen TUI
TUI interface for screen written in python, easily installable using pip

A modern screen session manager for Linux written in Python.

- Interactive curses UI
- Non-interactive CLI
- Colored output with `rich`
- Replacement for old Perl-based screenie

## Usage

```screen_tui          # launches UI
screen_tui -j NAME JOB  # creates session
```

## Installation
    python3 -m pip install --user --break-system-packages git+https://github.com/gitaware/screen_tui.git

## Uninstallation
    python3 -m pip uninstall --break-system-packages screen_tui
