import unittest
from pathlib import Path
from pto_ledger.core import accrue_months as evaluate
from pto_ledger.fixture_check import check


class CoreTests(unittest.TestCase):

    def test_cap_applies_before_usage_and_recovers_next_month(self):
        result = evaluate({"start_month": "2019-12-01", "opening_minutes": 95, "earn_minutes": 20, "cap_minutes": 100, "used_minutes": [30, 0]})
        self.assertEqual(result, {"months": [{"month": "2019-12-01", "earned_minutes": 5, "used_minutes": 30, "closing_minutes": 70},
            {"month": "2020-01-01", "earned_minutes": 20, "used_minutes": 0, "closing_minutes": 90}], "closing_minutes": 90})

    def test_zero_accrual_can_spend_the_exact_opening_balance(self):
        result = evaluate({"start_month": "2020-02-01", "opening_minutes": 90, "earn_minutes": 0, "cap_minutes": 100, "used_minutes": [90]})
        self.assertEqual(result["closing_minutes"], 0)

    def test_invalid_calendar_and_opening_balance_are_rejected(self):
        data = {"start_month": "2020-13-01", "opening_minutes": 0, "earn_minutes": 1, "cap_minutes": 100, "used_minutes": []}
        with self.assertRaises(ValueError):
            evaluate(data)
        data.update(start_month="2020-01-01", opening_minutes=101)
        with self.assertRaises(ValueError):
            evaluate(data)

    def test_complete_fixture_corpus(self):
        self.assertGreaterEqual(check(Path(__file__).resolve().parents[1] / "fixtures/cases.jsonl", evaluate), 500)


if __name__ == "__main__":
    unittest.main()
