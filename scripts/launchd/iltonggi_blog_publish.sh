#!/bin/bash
# iltonggi.ipe.rest blog publisher wrapper — template copy; the live one is ~/.ipe/bin/iltonggi_blog_publish.sh (see README.md here).
# launchd calls this at 12:00 / 12:30 / 13:30 KST. Outside 12:00-17:59 KST it exits at once (ILTONGGI_BLOG_ANYTIME=1 skips the check).
# It refreshes a dedicated clone and runs scripts/publish_blog.py (one post per KST day, so the retries are harmless). Extra args pass through (--dry-run).
set -u
ARGS="$*"
H="$(TZ=Asia/Seoul date +%H)"; H=$((10#$H))
if [ "${ILTONGGI_BLOG_ANYTIME:-0}" != "1" ] && { [ "$H" -lt 12 ] || [ "$H" -gt 17 ]; }; then exit 0; fi
CLONE="${ILTONGGI_BLOG_CLONE:-$HOME/.ipe/iltonggi-rest-publish}"
REMOTE="https://github.com/blessu76/iltonggi-rest.git"
# A failed run must never be silent (Davy 2026-10-29): macOS notification + ALERT file + ALERT history line (radar reads ~/.ipe/logs/*.ALERT) + optional hook (ILTONGGI_BLOG_ALERT_CMD gets the message as $1).
alert() {
  [ "$ARGS" = "--dry-run" ] && return 0
  local MSG="$2 (exit $1) $(TZ=Asia/Seoul date '+%F %H:%M') KST - see ~/.ipe/logs/iltonggi-blog-publish.log"
  echo "ALERT $MSG"; mkdir -p "$HOME/.ipe/logs"; echo "$MSG" > "$HOME/.ipe/logs/iltonggi-blog-publish.ALERT"
  echo "$MSG" >> "$HOME/.ipe/logs/iltonggi-blog-publish.ALERT.history"
  osascript -e "display notification \"$MSG\" with title \"iltonggi blog\"" >/dev/null 2>&1 || true
  [ -n "${ILTONGGI_BLOG_ALERT_CMD:-}" ] && $ILTONGGI_BLOG_ALERT_CMD "$MSG" || true
}
echo "=== $(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M:%S') KST blog publish tick"
if [ ! -d "$CLONE/.git" ]; then
  git clone --quiet "$REMOTE" "$CLONE" || { echo "ERROR clone failed"; alert 1 "clone failed"; exit 1; }
fi
git -C "$CLONE" fetch --quiet origin main && git -C "$CLONE" checkout --quiet main && git -C "$CLONE" reset --hard --quiet origin/main \
  || { echo "ERROR could not sync clone to origin/main"; alert 1 "clone sync to origin/main failed"; exit 1; }
[ -f "$CLONE/scripts/publish_blog.py" ] || { echo "publish_blog.py is not on main yet - nothing to do"; exit 0; }
cd "$CLONE" || exit 1
# The private ipe_web_kit is NOT in this public repo (vendor/ipe_web_kit/ is gitignored): on every tick make sure the clone has the kit
# that vendor/ipe_web_kit.lock pins, copying it from the local kit clone when missing or when the lock moved (2026-11-07 outage: kit absent -> every tick exit 1).
KIT="${ILTONGGI_WEB_KIT:-$HOME/Developer/ipe_web_kit}"
if ! python3 scripts/kit_lock.py check >/dev/null 2>&1; then
  echo "ipe_web_kit missing or off-lock - syncing from $KIT"
  python3 scripts/kit_lock.py sync --kit "$KIT" || { echo "ERROR kit sync failed"; alert 1 "ipe_web_kit sync failed"; exit 1; }
fi
python3 scripts/publish_blog.py "$@"; rc=$?
if [ "$rc" -ne 0 ]; then alert "$rc" "blog publish FAILED"; elif [ "$*" != "--dry-run" ]; then rm -f "$HOME/.ipe/logs/iltonggi-blog-publish.ALERT"; fi
exit $rc
