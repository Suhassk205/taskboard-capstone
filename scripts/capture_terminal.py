#!/usr/bin/env python3
"""Capture a macOS Terminal window displaying a saved, real command transcript.

Usage: python3 scripts/capture_terminal.py evidence/output.txt screenshots/output.png
The transcript is displayed verbatim; this tool does not invent command results.
Requires macOS Automation and Screen Recording access for Terminal/screencapture.
"""
import json
from pathlib import Path
import shlex
import subprocess
import sys
import time


def capture(transcript, output):
    transcript = Path(transcript).resolve(strict=True)
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    command = "clear\ncat " + shlex.quote(str(transcript))
    title = "Homework evidence - " + transcript.stem + " - " + str(time.time_ns())[-6:]
    script = f'''tell application "Terminal"
activate
set evidenceTab to do script {json.dumps(command)}
set number of columns of evidenceTab to 145
set number of rows of evidenceTab to 48
set custom title of evidenceTab to {json.dumps(title)}
delay 1
repeat with evidenceWindow in windows
if custom title of selected tab of evidenceWindow is {json.dumps(title)} then
set index of evidenceWindow to 1
return id of evidenceWindow
end if
end repeat
error "Evidence window not found"
end tell'''
    window = subprocess.check_output(["osascript", "-"], input=script, text=True).strip()
    time.sleep(1.2)
    subprocess.run(["screencapture", "-x", "-l", window, str(output)], check=True)
    if not output.exists() or output.stat().st_size < 1000:
        raise RuntimeError("Terminal screenshot was not captured")
    print(output)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    capture(sys.argv[1], sys.argv[2])
