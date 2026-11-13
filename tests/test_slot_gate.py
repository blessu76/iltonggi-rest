import datetime as dt
import json
import random
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ops"))
import slot_gate as sg  # noqa: E402

KST = sg.KST


def at(s):
    return dt.datetime.fromisoformat(s).astimezone(KST)


class SlotGate(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.state = self.tmp / "q" / "slot.json"
        self.calls = []

    def publisher(self, rc=0):
        def f(wrapper, dry):
            self.calls.append(wrapper)
            return rc
        return f

    def tick(self, now, rc=0):
        return sg.run(at(now), self.state, "w.sh", publisher=self.publisher(rc), rng=random.Random(1))

    def write(self, **kw):
        self.state.parent.mkdir(parents=True, exist_ok=True)
        self.state.write_text(json.dumps(kw), encoding="utf-8")

    def read(self):
        return json.loads(self.state.read_text(encoding="utf-8"))

    def test_pick_never_same_hour_as_yesterday_and_in_afternoon(self):
        rng = random.Random(7)
        for prev in ("12:00", "13:59", "15:30", "17:59", None):
            for _ in range(300):
                t = sg.pick_time(prev, rng)
                h = int(t[:2])
                self.assertTrue(12 <= h <= 17, t)
                if prev:
                    self.assertNotEqual(h, int(prev[:2]))

    def test_new_day_rolls_and_moves_yesterday_to_prev(self):
        self.write(date="2026-11-13", time="14:20", prev_date="2026-11-12", prev_time="16:00", published=True)
        self.tick("2026-11-14T12:00:00+09:00")
        s = self.read()
        self.assertEqual((s["date"], s["prev_date"], s["prev_time"]), ("2026-11-14", "2026-11-13", "14:20"))
        self.assertFalse(s["published"] and not self.calls)
        self.assertNotEqual(int(s["time"][:2]), 14)

    def test_same_day_keeps_the_slot(self):
        self.write(date="2026-11-14", time="16:40", prev_date="2026-11-13", prev_time="12:00", published=False)
        self.assertEqual(self.tick("2026-11-14T15:00:00+09:00"), 0)
        self.assertEqual(self.read()["time"], "16:40")
        self.assertEqual(self.calls, [])  # not yet

    def test_runs_once_due_and_marks_published(self):
        self.write(date="2026-11-14", time="14:10", prev_date=None, prev_time=None, published=False)
        self.assertEqual(self.tick("2026-11-14T14:15:00+09:00"), 0)
        self.assertEqual(len(self.calls), 1)
        self.assertTrue(self.read()["published"])
        self.tick("2026-11-14T14:30:00+09:00")
        self.assertEqual(len(self.calls), 1)  # already published -> ignored

    def test_failure_keeps_published_false_for_retry(self):
        self.write(date="2026-11-14", time="14:10", prev_date=None, prev_time=None, published=False)
        self.assertEqual(self.tick("2026-11-14T14:15:00+09:00", rc=1), 1)
        self.assertFalse(self.read()["published"])
        self.tick("2026-11-14T14:30:00+09:00")
        self.assertEqual(len(self.calls), 2)

    def test_missing_state_creates_today_and_outside_window_is_idle(self):
        self.tick("2026-11-14T11:45:00+09:00")
        self.assertEqual(self.read()["date"], "2026-11-14")
        self.assertEqual(self.calls, [])
        self.write(date="2026-11-14", time="17:59", prev_date=None, prev_time=None, published=False)
        self.tick("2026-11-14T19:00:00+09:00")
        self.assertEqual(self.calls, [])
        self.tick("2026-11-14T18:45:00+09:00")  # last tick still publishes a late retry
        self.assertEqual(len(self.calls), 1)

    def test_dry_run_writes_nothing(self):
        sg.run(at("2026-11-14T14:15:00+09:00"), self.state, "w.sh", dry_run=True, publisher=self.publisher())
        self.assertFalse(self.state.exists())


if __name__ == "__main__":
    unittest.main()
