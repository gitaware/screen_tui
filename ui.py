# screen_tui/ui.py
import curses
import os
from .core import get_sessions, attach_session, start_session

def main_menu(stdscr):
    curses.curs_set(0)
    current_row = 0
    error = None

    def draw_menu(sessions, highlight, err=None):
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(0, 0, "screen_tui - screen session manager (press q to quit)")
        for idx, (pid, name) in enumerate(sessions):
            line = f"{idx + 1}) {pid}.{name}"
            if idx == highlight:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(idx + 2, 2, line)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(idx + 2, 2, line)

        stdscr.addstr(len(sessions) + 4, 2, "n) New session")
        if err:
            stdscr.addstr(len(sessions) + 6, 2, f"Error: {err}", curses.color_pair(2))
        stdscr.refresh()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        sessions = get_sessions()
        draw_menu(sessions, current_row, error)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(sessions) - 1:
            current_row += 1
        elif key in (curses.KEY_ENTER, 10, 13):
            pid = sessions[current_row][0]
            code, msg = attach_session(pid)
            error = msg if code else None
        elif key == ord('n'):
            curses.echo()
            stdscr.clear()
            stdscr.addstr(0, 0, "Session name: ")
            name = stdscr.getstr(0, 15, 60).decode()
            stdscr.addstr(1, 0, "Job (blank for shell): ")
            job = stdscr.getstr(1, 24, 60).decode()
            curses.noecho()
            code, msg = start_session(name, job or os.environ.get('SHELL', '/bin/bash'))
            error = msg if code else None
        elif key == ord('q'):
            break
