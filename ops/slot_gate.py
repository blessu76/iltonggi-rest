#!/usr/bin/env python3
"""Random-afternoon slot gate for the daily journal post (Davy 2026-11-13: one post a day, random time in the afternoon, never the same hour as yesterday).

launchd calls this every 15 minutes from 12:00 to 18:45 KST (ops/rest.ipe.iltonggi-blog-publish.plist). State: ~/.ipe/queue/iltonggi/slot.json
    {"date": "YYYY-MM-DD", "time": "HH:MM", "prev_date": ..., "prev_time": ..., "published": bool}
On a new KST day it draws today's `time` in 12:00-17:59 (hour != yesterday's hour) and moves the old values to prev_*. Once now >= time and
published is false it runs the publish wrapper (~/.ipe/bin/iltonggi_blog_publish.sh -> scripts/publish_blog.py) and sets published=true on exit 0.
A failure leaves published=false, so the next 15-minute tick retries; the wrapper raises the ALERT itself.

    python3 ops/slot_gate.py [--dry-run] [--now 2026-11-13T14:10:00+09:00] [--state PATH] [--wrapper PATH]
"""
import argparse
import datetime as dt
import json
import os
import random
import subprocess
import sys
from pathlib import Path

KST = dt.timezone(dt.timedelta(hours=9))
STATE = Path.home() / ".ipe" / "queue" / "iltonggi" / "slot.json"
WRAPPER = Path.home() / ".ipe" / "bin" / "iltonggi_blog_publish.sh"
FIRST_HOUR, LAST_HOUR = 12, 17            # the drawn time lies in 12:00-17:59
WINDOW_END = (18, 45)                      # the last tick launchd makes


def load_state(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_state(path, state):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(path))


def pick_time(prev_time, rng=random):
    """A random HH:MM in 12:00-17:59 whose hour differs from prev_time's hour (any hour if there is no yesterday)."""
    hours = [h for h in range(FIRST_HOUR, LAST_HOUR + 1) if not (prev_time and int(prev_time[:2]) == h)]
    return "%02d:%02d" % (rng.choice(hours), rng.randrange(60))


def roll(state, today, rng=random):
    """New KST day -> draw today's slot and move the old one to prev_*. Same day -> unchanged. Returns (state, changed)."""
    if state.get("date") == today:
        return state, False
    return {"date": today, "time": pick_time(state.get("time"), rng),
            "prev_date": state.get("date"), "prev_time": state.get("time"), "published": False}, True


def in_window(now):
    return (FIRST_HOUR, 0) <= (now.hour, now.minute) <= WINDOW_END


def due(state, now):
    """True when today's slot has passed and nothing was published yet."""
    return (not state.get("published")) and "%02d:%02d" % (now.hour, now.minute) >= state["time"]


def publish(wrapper, dry_run=False):
    env = dict(os.environ, ILTONGGI_BLOG_ANYTIME="1")  # the gate owns the time window; the wrapper's 12-17h guard would block 18:00-18:45 retries
    cmd = ["/bin/bash", str(wrapper)] + (["--dry-run"] if dry_run else [])
    print("$ " + " ".join(cmd), flush=True)
    return subprocess.run(cmd, env=env).returncode


def run(now, state_path=STATE, wrapper=WRAPPER, dry_run=False, rng=random, publisher=publish):
    """One tick. Returns the process exit code (0 = nothing wrong, including 'not yet' and 'already published')."""
    today = now.date().isoformat()
    state, changed = roll(load_state(state_path), today, rng)
    if changed and not dry_run:
        save_state(state_path, state)
    if not in_window(now):
        print("slot_gate: %s is outside 12:00-18:45 KST - nothing to do" % now.strftime("%H:%M"))
        return 0
    if state.get("published"):
        print("slot_gate: already published today (%s) - ignoring" % today)
        return 0
    if not due(state, now):
        print("slot_gate: today's slot is %s - not yet (%s)" % (state["time"], now.strftime("%H:%M")))
        return 0
    rc = publisher(wrapper, dry_run)
    if rc == 0 and not dry_run:
        state["published"] = True
        save_state(state_path, state)
        print("slot_gate: published for %s (slot %s)" % (today, state["time"]))
    elif rc != 0:
        print("slot_gate: publish failed (exit %d) - retrying on the next tick" % rc, file=sys.stderr)
    return rc


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--now", help="ISO time with +09:00 (tests); default now")
    ap.add_argument("--state", default=str(STATE))
    ap.add_argument("--wrapper", default=str(WRAPPER))
    ap.add_argument("--dry-run", action="store_true", help="roll in memory and pass --dry-run to the wrapper; writes nothing")
    a = ap.parse_args(argv)
    now = dt.datetime.fromisoformat(a.now).astimezone(KST) if a.now else dt.datetime.now(KST)
    return run(now, a.state, a.wrapper, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
