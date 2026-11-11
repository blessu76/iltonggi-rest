#!/bin/bash
# Green gate for iltonggi-rest — run before every commit. Exit 0 = green.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== 1/4 kit"; python3 scripts/kit_lock.py check
echo "== 2/4 release notes"; PYTHONPATH=vendor python3 -m ipe_web_kit.releases check content/releases.json --require-langs ko,en
echo "== 3/4 unit tests"; python3 -m unittest discover -s tests -q
echo "== 4/4 build is up to date"; python3 scripts/build_site.py --check
echo "GREEN"
