import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import fetch_weather as fw  # noqa: E402


def met_doc(symbol="clearsky_day", temp=12.4, wind=3.26, precip=0.0, time="2026-10-28T11:00:00Z"):
    return {"properties": {"timeseries": [{
        "time": time,
        "data": {"instant": {"details": {"air_temperature": temp, "wind_speed": wind}},
                 "next_1_hours": {"summary": {"symbol_code": symbol}, "details": {"precipitation_amount": precip}}}}]}}


REGIONS = [{"id": "a", "lat": 1.0, "lon": 2.0}, {"id": "b", "lat": 3.0, "lon": 4.0}]
NOW = datetime(2026, 10, 28, 12, 7, tzinfo=timezone.utc)


class Mapping(unittest.TestCase):
    def test_symbol_to_cond(self):
        table = {
            "clearsky_day": "clear", "fair_night": "clear", "partlycloudy_day": "cloudy", "cloudy": "cloudy",
            "fog": "fog", "lightrain": "rain", "rain": "rain", "heavyrainshowers_day": "rain",
            "sleet": "rain", "lightsleetshowers_night": "rain", "snow": "snow", "heavysnowshowers_day": "snow",
            "rainandthunder": "storm", "lightssleetshowersandthunder_day": "storm", "heavysnowandthunder": "storm",
            "": "clear", None: "clear", "somethingnew": "clear",
        }
        for code, want in table.items():
            self.assertEqual(fw.cond_from_symbol(code), want, code)

    def test_every_result_is_a_known_cond(self):
        for code in ["clearsky_day", "rain", "snow", "fog", "cloudy", "heavyrainandthunder"]:
            self.assertIn(fw.cond_from_symbol(code), fw.CONDS)


class Parse(unittest.TestCase):
    def test_entry_shape_and_rounding(self):
        e = fw.parse_region(met_doc("lightrain", 12.5, 3.26, 0.44), "a")
        self.assertEqual(e, {"cond": "rain", "t": 12, "wind": 3.3, "precip": 0.4, "at": "2026-10-28T11:00:00Z"})
        self.assertTrue(fw.valid_entry(e))

    def test_negative_temperature(self):
        self.assertEqual(fw.parse_region(met_doc("snow", -3.6), "a")["t"], -4)

    def test_missing_details_raises(self):
        doc = met_doc()
        del doc["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]
        with self.assertRaises(ValueError):
            fw.parse_region(doc, "a")


class Build(unittest.TestCase):
    def run_build(self, fetch, prev):
        return fw.build(REGIONS, prev, fetch=fetch, gap=0, now=NOW, sleep=lambda s: None)

    def test_schema(self):
        doc, fresh = self.run_build(lambda url: met_doc(), {})
        self.assertEqual(fresh, 2)
        self.assertEqual(set(doc), {"v", "updated", "source", "attribution", "regions"})
        self.assertEqual(doc["v"], 1)
        self.assertEqual(doc["updated"], "2026-10-28T12:07:00Z")
        self.assertEqual(doc["source"], "MET Norway")
        self.assertIn("CC BY 4.0", doc["attribution"])
        self.assertEqual(set(doc["regions"]), {"a", "b"})
        for e in doc["regions"].values():
            self.assertTrue(fw.valid_entry(e))
            self.assertEqual(set(e), {"cond", "t", "wind", "precip", "at"})

    def test_request_url_has_four_decimals(self):
        seen = []
        self.run_build(lambda url: seen.append(url) or met_doc(), {})
        self.assertIn("lat=1.0000&lon=2.0000", seen[0])

    def test_failed_region_keeps_previous(self):
        old = {"cond": "snow", "t": -2, "wind": 1.0, "precip": 0.2, "at": "2026-10-28T08:00:00Z"}

        def fetch(url):
            if "lat=3.0000" in url:
                raise OSError("boom")
            return met_doc("rain")
        doc, fresh = self.run_build(fetch, {"b": old})
        self.assertEqual(fresh, 1)
        self.assertEqual(doc["regions"]["a"]["cond"], "rain")
        self.assertEqual(doc["regions"]["b"], old)

    def test_failed_region_without_previous_is_omitted(self):
        def fetch(url):
            if "lat=3.0000" in url:
                raise OSError("boom")
            return met_doc()
        doc, _ = self.run_build(fetch, {})
        self.assertEqual(set(doc["regions"]), {"a"})

    def test_all_failed_returns_nothing_fresh(self):
        def fetch(url):
            raise OSError("down")
        doc, fresh = self.run_build(fetch, {})
        self.assertIsNone(doc)
        self.assertEqual(fresh, 0)


class Cli(unittest.TestCase):
    def test_all_failed_keeps_previous_file(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            prev = {"v": 1, "updated": "2026-10-28T10:07:00Z", "source": "MET Norway", "attribution": "x",
                    "regions": {"a": {"cond": "fog", "t": 5, "wind": 0.5, "precip": 0.0, "at": "2026-10-28T10:00:00Z"}}}
            (d / "prev.json").write_text(json.dumps(prev))
            (d / "regions.json").write_text(json.dumps({"regions": REGIONS}))
            orig = fw.fetch_json
            fw.fetch_json = lambda url, timeout=20: (_ for _ in ()).throw(OSError("down"))
            orig_gap, orig_sleep = fw.REQUEST_GAP_S, fw.time.sleep
            fw.REQUEST_GAP_S = 0
            try:
                rc = fw.main(["--out", str(d / "out" / "weather.json"), "--prev", str(d / "prev.json"),
                              "--regions", str(d / "regions.json")])
            finally:
                fw.fetch_json = orig
                fw.REQUEST_GAP_S = orig_gap
            self.assertEqual(rc, 0)
            self.assertEqual(json.loads((d / "out" / "weather.json").read_text()), prev)


class RegionsFile(unittest.TestCase):
    def test_regions_json(self):
        regs = json.loads((ROOT / "regions.json").read_text(encoding="utf-8"))["regions"]
        self.assertEqual(len(regs), 24)
        ids = [r["id"] for r in regs]
        self.assertEqual(len(set(ids)), 24)
        for r in regs:
            self.assertRegex(r["id"], r"^[a-z]+$")
            self.assertTrue(-90 <= r["lat"] <= 90 and -180 <= r["lon"] <= 180)
            self.assertEqual(r["lat"], round(r["lat"], 4))
            self.assertEqual(r["lon"], round(r["lon"], 4))
            self.assertRegex(r["tz"], r"^[A-Za-z]+/[A-Za-z_]+$")


if __name__ == "__main__":
    unittest.main()
