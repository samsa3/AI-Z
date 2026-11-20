"""Usage (from repo root):
    python -m agent.brane_agent.cli data/synthetic/01_clean.txt            # real BRANE from .env
    python -m agent.brane_agent.cli data/synthetic/02_protected.txt --mock # offline mock gateway
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from .gateway import BraneGateway
from .mock_brane import MockBrane
from .pipeline import ROOT, run

DEFAULT_CRITERIA = [  # placeholder until the use case is confirmed
    "At least 3 years of project management experience",
    "Degree in business informatics, computer science or a related field",
    "Experience with agile methods",
]


def load_env(path: Path = ROOT / ".env") -> None:
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def main() -> None:
    p = argparse.ArgumentParser(description="Run the agent on one synthetic document.")
    p.add_argument("file")
    p.add_argument("--mock", action="store_true", help="use the local mock gateway (offline)")
    p.add_argument("--brane-down", action="store_true", help="simulate BRANE unavailable")
    p.add_argument("--show-payload", action="store_true", help="print what was handed to BRANE")
    a = p.parse_args()

    load_env()
    mock = MockBrane() if a.mock else None
    url = "http://127.0.0.1:9" if a.brane_down else (mock.url if mock else None)
    gw = BraneGateway(url=url, timeout=3)
    try:
        r = run(Path(a.file).read_text(encoding="utf-8"), DEFAULT_CRITERIA, gw, test_id=Path(a.file).stem)
    finally:
        if mock:
            mock.close()

    print(f"run_id   : {r.run_id}\ndecision : {r.decision}\nreason   : {r.reason}")
    for e in r.events:
        print(f"  {e['rule']:<4} {e['measure']:<10} {e['category']:<28} x{e['count']}")
    if a.show_payload and r.payload_sent:
        print("\n--- payload handed to BRANE ---\n" + r.payload_sent)
    if r.reviewer_view:
        print("\n--- reviewer view (local only) ---\n" + r.reviewer_view)


if __name__ == "__main__":
    main()
