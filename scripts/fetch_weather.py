#!/usr/bin/env python3
"""Fetch current weather for every region in regions.json from MET Norway and write weather.json.

    python3 scripts/fetch_weather.py --out OUT/weather.json [--prev URL_OR_FILE]

MET Norway Locationforecast 2.0 (https://api.met.no, no key, CC BY 4.0). One identified request per region,
spaced out. A region that fails keeps its previous value (read from --prev, normally the live weather.json);
if every region fails the output is left as it is (a copy of --prev when there is one, else no file).
The app never calls MET itself: it only downloads the generated weather.json. Stdlib only, Python 3.8+.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=%.4f&lon=%.4f"
USER_AGENT = "Iltonggi/1.0 (+https://iltonggi.ipe.rest; ipe.haven@gmail.com)"
SOURCE = "MET Norway"
ATTRIBUTION = "Weather data: MET Norway (CC BY 4.0)"
CONDS = ("clear", "cloudy", "rain", "snow", "fog", "storm")
REQUEST_GAP_S = 1.0


def cond_from_symbol(code):
    """MET symbol_code ('lightrainshowers_day', 'heavysnowandthunder', ...) -> one of CONDS."""
    base = (code or "").split("_")[0]
    if "thunder" in base:
        return "storm"
    if "snow" in base:
        return "snow"
    if "sleet" in base or "rain" in base:   # sleet is wet and cold: counts as rain
        return "rain"
    if base == "fog":
        return "fog"
    if base in ("partlycloudy", "cloudy"):
        return "cloudy"
    return "clear"  # clearsky, fair, unknown


def parse_region(doc, region_id):
    """The first (nearest) timeseries entry of a locationforecast compact document -> region entry."""
    ts = doc["properties"]["timeseries"][0]
    det = ts["data"]["instant"]["details"]
    nxt = ts["data"].get("next_1_hours") or ts["data"].get("next_6_hours") or {}
    symbol = nxt.get("summary", {}).get("symbol_code")
    precip = nxt.get("details", {}).get("precipitation_amount", 0.0)
    if "air_temperature" not in det or "wind_speed" not in det:
        raise ValueError("%s: missing instant details" % region_id)
    when = datetime.strptime(ts["time"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return {
        "cond": cond_from_symbol(symbol),
        "t": int(round(det["air_temperature"])),
        "wind": round(float(det["wind_speed"]), 1),
        "precip": round(float(precip), 1),
        "at": when.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def valid_entry(e):
    return (isinstance(e, dict) and e.get("cond") in CONDS and isinstance(e.get("t"), int)
            and isinstance(e.get("wind"), (int, float)) and isinstance(e.get("precip"), (int, float))
            and isinstance(e.get("at"), str))


def fetch_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def load_prev(src):
    """Previous weather.json from a URL or a path; anything unreadable/invalid -> {}."""
    if not src:
        return {}
    try:
        doc = fetch_json(src) if src.startswith("http") else json.loads(Path(src).read_text(encoding="utf-8"))
        regs = doc.get("regions", {})
        return {k: v for k, v in regs.items() if valid_entry(v)}
    except Exception as e:  # noqa: BLE001 - a missing previous file is normal on the first run
        print("no previous weather (%s)" % e, file=sys.stderr)
        return {}


def build(regions, prev, fetch=None, gap=None, now=None, sleep=None):
    """-> (document or None, number of regions fetched fresh). None when nothing could be fetched and no prev."""
    fetch = fetch or fetch_json
    gap = REQUEST_GAP_S if gap is None else gap
    sleep = sleep or time.sleep
    out, fresh = {}, 0
    for i, r in enumerate(regions):
        if i:
            sleep(gap)
        try:
            out[r["id"]] = parse_region(fetch(ENDPOINT % (r["lat"], r["lon"])), r["id"])
            fresh += 1
        except Exception as e:  # noqa: BLE001 - keep the old value for this region
            print("region %s failed: %s" % (r["id"], e), file=sys.stderr)
            if r["id"] in prev:
                out[r["id"]] = prev[r["id"]]
    if not out:
        return None, 0
    now = now or datetime.now(timezone.utc)
    return {"v": 1, "updated": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": SOURCE,
            "attribution": ATTRIBUTION, "regions": out}, fresh


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--prev", default="")
    ap.add_argument("--regions", default=str(ROOT / "regions.json"))
    a = ap.parse_args(argv)
    regions = json.loads(Path(a.regions).read_text(encoding="utf-8"))["regions"]
    prev = load_prev(a.prev)
    doc, fresh = build(regions, prev)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if fresh == 0:
        # every request failed: leave the previous file as it was (published unchanged), or none at all
        print("all %d regions failed — keeping previous weather.json" % len(regions), file=sys.stderr)
        if prev:
            try:
                prev_doc = fetch_json(a.prev) if a.prev.startswith("http") else json.loads(Path(a.prev).read_text(encoding="utf-8"))
                out.write_text(json.dumps(prev_doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
            except Exception as e:  # noqa: BLE001
                print("could not re-read previous: %s" % e, file=sys.stderr)
        return 0
    out.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print("wrote %s: %d/%d regions fresh" % (out, fresh, len(regions)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
