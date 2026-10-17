"""Record real commands and output for the homework verification scripts."""
from datetime import datetime
from pathlib import Path
import shlex
import subprocess
import time
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
CONTEXT = "kind-session13"


class Evidence:
    def __init__(self, session, name, title, append=False, context=CONTEXT):
        self.path = ROOT / session / "evidence" / f"{name}.txt"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        header = f"{title}\nActual command transcript; {datetime.now(ZoneInfo('Asia/Kolkata')).isoformat()}\nContext: {context}\n\n"
        with self.path.open("a" if append else "w") as f:
            f.write(header)

    def note(self, text):
        with self.path.open("a") as f:
            f.write(text + "\n")
        print(text, flush=True)

    def run(self, args, check=True, cwd=ROOT, timeout=180, input=None, expected_exit=0):
        self.note("$ " + shlex.join(str(x) for x in args))
        result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=timeout, input=input)
        self.note(result.stdout.rstrip())
        self.note(f"[exit {result.returncode}]\n")
        if check and result.returncode != expected_exit:
            raise RuntimeError(f"Command failed: {args}; see {self.path}")
        return result.stdout

    def k(self, ns, *args, **kwargs):
        return self.run(["kubectl", "--context", CONTEXT, "-n", ns, *args], **kwargs)


def raw_k(ns, *args):
    return subprocess.check_output(["kubectl", "--context", CONTEXT, "-n", ns, *args], text=True)


def wait_until(predicate, timeout=180, interval=5):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(interval)
    raise TimeoutError("Expected lab condition was not observed before timeout")
