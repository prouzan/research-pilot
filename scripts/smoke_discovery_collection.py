from __future__ import annotations

import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from researchpilot.discovery.venue_collector import collect_venue_papers
from researchpilot.discovery.venue_collector import plan_venue_collection


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Smoke test for unified Research Discovery planning and collection schema.",
    )
    parser.add_argument(
        "topic",
        nargs="?",
        default="formal verification and large language models",
        help="Research topic to plan and collect for.",
    )
    return parser


def main(argv: list[str]) -> int:
    args = _build_parser().parse_args(argv[1:])
    plan = plan_venue_collection(
        topic=args.topic,
        domains=["ai", "formal_methods"],
        keywords=["formal specification", "verified code generation"],
        max_venues=4,
    )
    venues = plan.get("venues", [])
    if not venues:
        print("Error: venue plan is empty.", file=sys.stderr)
        return 1

    collection = collect_venue_papers(
        topic=args.topic,
        domains=["ai", "formal_methods"],
        keywords=["formal specification", "verified code generation"],
        years=[2026],
        include_arxiv=False,
        include_openreview=False,
        include_openalex=False,
        include_semantic_scholar=False,
        max_venues=2,
        max_results_per_venue=1,
        max_total=3,
    )
    required_keys = {"topic", "plan", "papers", "source_config", "warnings"}
    missing = required_keys.difference(collection)
    if missing:
        print(f"Error: collection missing keys: {sorted(missing)}", file=sys.stderr)
        return 1

    print(f"topic={collection['topic']}")
    print(f"planned_venues={len(venues)}")
    print(f"collection_papers={collection.get('paper_count', 0)}")
    print(f"source_config={collection.get('source_config', {})}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
