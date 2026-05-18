from __future__ import annotations

from pathlib import Path
import sys
import tempfile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from researchpilot.storage.paper_labels import all_paper_labels
from researchpilot.storage.paper_labels import labels_for_paper
from researchpilot.storage.paper_labels import load_paper_labels
from researchpilot.storage.paper_labels import normalize_labels
from researchpilot.storage.paper_labels import save_paper_labels


def main() -> int:
    labels = {
        "paper-a": normalize_labels("formal verification, LLM code"),
        "paper-b": normalize_labels(["survey", "Formal Verification"]),
    }
    output_path = Path(tempfile.gettempdir()) / "researchpilot_paper_labels_smoke.json"
    save_paper_labels(labels, path=output_path)
    loaded = load_paper_labels(path=output_path)

    if labels_for_paper("paper-a", loaded) != ["formal verification", "LLM code"]:
        print("Error: labels_for_paper returned unexpected labels.", file=sys.stderr)
        return 1
    available = all_paper_labels(loaded)
    if "survey" not in available:
        print("Error: all_paper_labels missing expected label.", file=sys.stderr)
        return 1

    print(f"papers={len(loaded)}")
    print(f"labels={', '.join(available)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
