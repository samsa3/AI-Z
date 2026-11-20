"""Five pass/fail security tests (tests/test-protocol.md) against the local mock gateway.

Run from repo root:  python -m unittest discover -s tests/security -v
The mock records everything it receives, so `mock.sent_text()` is exactly what
would have reached the external model through BRANE.
"""
import re
import unittest
from pathlib import Path

from agent.brane_agent.gateway import BraneGateway
from agent.brane_agent.mock_brane import MockBrane
from agent.brane_agent.pipeline import run

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "synthetic"
CRITERIA = ["At least 3 years of project management experience", "Relevant degree"]

NAME_VARIANTS = ["Mira Fictus", "Fictus", "Mira", "M. Fictus", "Ms Fictus", "Fictus, Mira"]


def read(name):
    return (DATA / name).read_text(encoding="utf-8")


class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.mock = MockBrane()
        self.gw = BraneGateway(url=self.mock.url, api_key="test", timeout=3)

    def tearDown(self):
        self.mock.close()

    def assert_no_pii(self, sent):
        low = sent.lower()
        for v in NAME_VARIANTS:
            self.assertIsNone(re.search(r"(?<![\w])" + re.escape(v.lower()) + r"(?![\w])", low), f"name leaked: {v}")
        for leak in ["@example.org", "612 345 678", "0061-2345-678", "teststraat", "test123456", "xx00 test"]:
            self.assertNotIn(leak, low, f"leak: {leak}")

    def test_T1_permitted_control_case(self):
        r = run(read("01_clean.txt"), CRITERIA, self.gw, test_id="T1")
        self.assertEqual(r.decision, "ALLOW")
        self.assertEqual(len(self.mock.received), 1)
        self.assertIn("Five years of project management", self.mock.sent_text())
        self.assertIn("RECOMMENDATION ONLY", r.reviewer_view)

    def test_T2_protected_data(self):
        r = run(read("02_protected.txt"), CRITERIA, self.gw, test_id="T2")
        self.assertEqual(r.decision, "PROTECT")
        sent = self.mock.sent_text()
        self.assert_no_pii(sent)
        for word in ["burnout", "sick leave", "diagnosis"]:
            self.assertNotIn(word, sent.lower())
        self.assertIn("PERSON_01", sent)
        self.assertIn("Five years of project management", sent)  # task data still flows
        self.assertEqual({e["rule"] for e in r.events} >= {"R2", "R3", "R5", "R6"}, True)

    def test_T3_repeated_details(self):
        r = run(read("03_repeated.txt"), CRITERIA, self.gw, test_id="T3")
        sent = self.mock.sent_text()
        self.assert_no_pii(sent)
        self.assertGreaterEqual(sent.count("PERSON_01"), 6)
        self.assertNotIn("PERSON_02", sent)  # every variant maps to the SAME pseudonym

    def test_T4_bypass_attempt(self):
        r = run(read("04_bypass.txt"), CRITERIA, self.gw, test_id="T4")
        sent = self.mock.sent_text().lower()
        self.assert_no_pii(sent)
        for phrase in ["ignore previous instructions", "print the original", "regardless of the criteria"]:
            self.assertNotIn(phrase, sent)
        self.assertIn("R9", {e["rule"] for e in r.events})
        self.assertIn("untrusted data", sent)  # system prompt hardening present

    def test_T5_check_failure_unreachable(self):
        self.mock.close()
        gw = BraneGateway(url=self.mock.url, api_key="test", timeout=2)
        r = run(read("05_check_failure.txt"), CRITERIA, gw, test_id="T5")
        self.assertEqual(r.decision, "BLOCK")
        self.assertIsNone(r.payload_sent)
        self.assertIn("R10", {e["rule"] for e in r.events})
        self.mock = MockBrane()  # so tearDown has something to close

    def test_T5b_check_failure_server_error(self):
        self.mock.status = 500
        r = run(read("05_check_failure.txt"), CRITERIA, self.gw, test_id="T5b")
        self.assertEqual(r.decision, "BLOCK")
        self.assertIsNone(r.payload_sent)

    def test_T5c_not_configured(self):
        r = run(read("05_check_failure.txt"), CRITERIA, BraneGateway(url="", api_key=""), test_id="T5c")
        self.assertEqual(r.decision, "BLOCK")
        self.assertEqual(len(self.mock.received), 0)


class NoDirectModelAccess(unittest.TestCase):
    def test_no_openai_client_or_endpoint_in_code(self):
        for py in (ROOT / "agent").rglob("*.py"):
            src = py.read_text(encoding="utf-8").lower()
            self.assertNotIn("api.openai.com", src, py)
            self.assertNotIn("import openai", src, py)
            self.assertNotIn("openai_api_key", src, py)


if __name__ == "__main__":
    unittest.main()
