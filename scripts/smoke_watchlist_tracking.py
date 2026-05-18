from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from researchpilot.watchlist import tracker


def main() -> int:
    item = {
        "name": "Demo Verification Group",
        "type": "research_group",
        "authors": ["Ada Lovelace"],
        "institutions": ["Demo University"],
        "keywords": ["formal verification", "code generation"],
        "homepage_urls": ["https://example.org/lab"],
    }
    tracker.search_semantic_scholar = lambda *args, **kwargs: [
        {
            "semantic_scholar_paper_id": "S2-SMOKE",
            "source": "semantic_scholar",
            "source_url": "https://example.org/paper",
            "pdf_url": "",
            "title": "Verified Code Generation with Formal Specifications",
            "authors": ["Ada Lovelace"],
            "year": 2026,
            "publication_date": "2026-05-01",
            "venue": "Demo Venue",
            "abstract": "A recent paper on LLM code generation and formal verification.",
            "cited_by_count": 0,
            "collection_scope": "watchlist_tracking",
        }
    ]
    tracker.search_openalex_watch_papers = lambda *args, **kwargs: []

    output_path = Path(tempfile.gettempdir()) / "researchpilot_watchlist_tracking_smoke.json"
    output_path.unlink(missing_ok=True)
    result = tracker.track_watch_item(item, path=str(output_path))
    if result.get("paper_count") != 1:
        print(f"Error: expected 1 tracked paper, got {result.get('paper_count')}", file=sys.stderr)
        print(f"warnings={result.get('warnings', [])}", file=sys.stderr)
        print(f"query={result.get('query', '')}", file=sys.stderr)
        return 1
    paper_id = result["papers"][0]["paper_id"]
    tracker.dismiss_watch_paper(item, paper_id, path=str(output_path))
    state = tracker.load_watchlist_tracking(str(output_path))
    row = next(iter(state.values()))
    if paper_id not in row.get("dismissed_paper_ids", []):
        print("Error: dismissed paper id was not persisted.", file=sys.stderr)
        return 1

    print(json.dumps({"paper_count": result["paper_count"], "paper_id": paper_id}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
