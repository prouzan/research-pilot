from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from researchpilot.cards.metadata_cards import metadata_paper_id
from researchpilot.cards.metadata_cards import paper_card_from_metadata


def main() -> int:
    paper = {
        "source": "semantic_scholar",
        "source_url": "https://example.org/paper",
        "pdf_url": "https://example.org/paper.pdf",
        "semantic_scholar_paper_id": "S2-DEMO",
        "title": "A Demonstration Paper for Metadata Cards",
        "authors": ["Ada Lovelace", "Alan Turing"],
        "year": 2026,
        "publication_date": "2026-05-01",
        "venue": "Demo Venue",
        "abstract": "This paper studies paper card generation from discovery metadata.",
        "matched_keywords": ["paper card", "metadata"],
    }
    paper_id = metadata_paper_id(paper)
    card = paper_card_from_metadata(paper, topic="metadata card smoke test")
    if card.get("paper_id") != paper_id:
        print("Error: paper_id mismatch.", file=sys.stderr)
        return 1
    if not isinstance(card.get("zh"), dict):
        print("Error: bilingual zh field missing.", file=sys.stderr)
        return 1
    if not card.get("source_metadata", {}).get("source_url"):
        print("Error: source metadata missing.", file=sys.stderr)
        return 1

    print(f"paper_id={paper_id}")
    print(f"title={card.get('title', '')}")
    print(f"has_zh={bool(card.get('zh'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
