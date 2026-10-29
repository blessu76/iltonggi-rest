#!/bin/sh
# usage: scripts/add_release.sh <build> <notes.md> [shots_dir]   (see add_release.py)
exec python3 "$(dirname "$0")/add_release.py" "$@"
