# screen_tui/ui.py
import curses
import os
from .core import get_sessions, attach_session, start_session

def main_menu(stdscr):
    curses.curs_set(0)
    current_row = 0
    error = None
    number_buffer = ""  # store digits + optional x/d

    def draw_menu(sessions, highlight, err=None, numbuf=""):
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
        if numbuf:
            stdscr.addstr(len(sessions) + 5, 2, f"Selected: {numbuf}", curses.color_pair(3))
        if err:
            stdscr.addstr(len(sessions) + 6, 2, f"Error: {err}", curses.color_pair(2))
        stdscr.refresh()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    while True:
        sessions = get_sessions()
        draw_menu(sessions, current_row, error, number_buffer)

        key = stdscr.getch()

        # Handle typing: digits or x/d after digits
        if ord('0') <= key <= ord('9'):
            number_buffer += chr(key)
            continue
        elif key in (ord('x'), ord('d')) and number_buffer.isdigit():
            number_buffer += chr(key)
            continue

        if key in (curses.KEY_ENTER, 10, 13):
            if number_buffer:
                # Parse number and optional suffix
                import re
                m = re.match(r"^(\d+)([xd])?$", number_buffer)
                if m:
                    idx = int(m.group(1)) - 1
                    mode = m.group(2) or ''
                    if 0 <= idx < len(sessions):
                        pid = sessions[idx][0]
                        code, msg = attach_session(pid, mode)
                        error = msg if code else None
                    else:
                        error = f"Incorrect selection: {number_buffer}"
                else:
                    error = f"Incorrect selection: {number_buffer}"
                number_buffer = ""
            else:
                pid = sessions[current_row][0]
                code, msg = attach_session(pid)
                error = msg if code else None

        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(sessions) - 1:
            current_row += 1
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
        else:
            number_buffer = ""  # reset if invalid key

