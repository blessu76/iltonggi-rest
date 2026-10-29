#!/bin/bash
# iltonggi.ipe.rest blog publisher wrapper — template copy; the live one is ~/.ipe/bin/iltonggi_blog_publish.sh (see README.md here).
# launchd calls this at 12:00 / 12:30 / 13:30 KST. Outside 12:00-17:59 KST it exits at once (ILTONGGI_BLOG_ANYTIME=1 skips the check).
# It refreshes a dedicated clone and runs scripts/publish_blog.py (one post per KST day, so the retries are harmless). Extra args pass through (--dry-run).
set -u
H="$(TZ=Asia/Seoul date +%H)"; H=$((10#$H))
if [ "${ILTONGGI_BLOG_ANYTIME:-0}" != "1" ] && { [ "$H" -lt 12 ] || [ "$H" -gt 17 ]; }; then exit 0; fi
CLONE="${ILTONGGI_BLOG_CLONE:-$HOME/.ipe/iltonggi-rest-publish}"
REMOTE="https://github.com/blessu76/iltonggi-rest.git"
echo "=== $(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M:%S') KST blog publish tick"
if [ ! -d "$CLONE/.git" ]; then
  git clone --quiet "$REMOTE" "$CLONE" || { echo "ERROR clone failed"; exit 1; }
fi
git -C "$CLONE" fetch --quiet origin main && git -C "$CLONE" checkout --quiet main && git -C "$CLONE" reset --hard --quiet origin/main \
  || { echo "ERROR could not sync clone to origin/main"; exit 1; }
[ -f "$CLONE/scripts/publish_blog.py" ] || { echo "publish_blog.py is not on main yet - nothing to do"; exit 0; }
cd "$CLONE" && exec python3 scripts/publish_blog.py "$@"
