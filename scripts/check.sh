#!/bin/bash
# Green gate for iltonggi-rest — run before every commit. Exit 0 = green.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== 0/3 kit"; python3 scripts/kit_lock.py check
echo "== 1/3 unit tests"; python3 -m unittest discover -s tests -q
echo "== 2/3 committed pages up to date"; python3 scripts/build_site.py --check
echo GREEN
