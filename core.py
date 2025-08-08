# screen_tui/core.py
import subprocess
import os
import time

SCREEN_CMD = "screen"

def get_sessions():
    try:
        output = subprocess.check_output([SCREEN_CMD, '-ls'], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output

    sessions = []
    for line in output.splitlines():
        line = line.strip()
        if line and "." in line and ("(Attached)" in line or "(Detached)" in line):
            parts = line.split()
            pid_name = parts[0]
            if '.' in pid_name:
                pid, name = pid_name.split('.', 1)
                sessions.append([int(pid), name])
    sessions.sort(key=lambda x: x[1])
    return sessions

def attach_session(pid, mode=''):
    cmd = [SCREEN_CMD]
    if mode == 'x':
        cmd += ['-x', str(pid)]
    elif mode == 'd':
        cmd += ['-rd', str(pid)]
    else:
        cmd += ['-r', str(pid)]

    t0 = int(time.time())
    try:
        subprocess.run(cmd, check=True)
        return 0, ''
    except subprocess.CalledProcessError as e:
        if t0 == int(time.time()):
            return e.returncode, f"Failed to attach session with PID {pid}:\n{e}"
        return 0, ''

def start_session(name, job):
    if not name.strip():
        return 1, "Non-empty session name expected!"
    try:
        subprocess.run([SCREEN_CMD, '-S', name, '-dm'] + job.split(), check=True)
        return 0, ''
    except subprocess.CalledProcessError as e:
        return e.returncode, f"Failed to start session: {e}"
