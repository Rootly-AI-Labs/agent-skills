#!/usr/bin/env python3
"""Recollect durable per-case results without replacing a partial run index.

Does not rerun or regrade cases, and does not certify that a suite is complete.
Useful when the initiating terminal detached before the aggregate was finalized.
"""

import argparse
import json
from pathlib import Path


def collect(folder):
    results = [json.loads(path.read_text()) for path in sorted(folder.glob("*/result.json"))]
    if not results:
        raise ValueError("No per-case results found")
    identities = [(r["client"], r["case"], r.get("repeat", 1)) for r in results]
    if len(set(identities)) != len(identities):
        raise ValueError("Duplicate case/client result")
    with (folder / "collected-results.json").open("x") as output:
        output.write(json.dumps(results, indent=2) + "\n")
    return len(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    args = parser.parse_args()
    print(f"Collected {collect(args.folder)} per-case results; no regrading or completeness claim")
