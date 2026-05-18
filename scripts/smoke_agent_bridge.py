from __future__ import annotations

from pathlib import Path
import shutil
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from researchpilot.agent_bridge import agent_bridge_status
from researchpilot.agent_bridge import queue_agent_task


def main() -> int:
    status = agent_bridge_status()
    task = queue_agent_task(
        task_type="smoke_test",
        provider="queue",
        prompt="Smoke test prompt. No model execution required.",
        payload={"source": "scripts/smoke_agent_bridge.py"},
    )
    if task.get("status") != "queued":
        print("Error: queued task did not report queued status.", file=sys.stderr)
        return 1
    prompt_path = Path(task.get("prompt_path", ""))
    if not prompt_path.exists():
        print("Error: queued task prompt file is missing.", file=sys.stderr)
        return 1
    task_dir = prompt_path.parent

    print(f"codex_available={status.get('codex_available')}")
    print(f"opencode_available={status.get('opencode_available')}")
    print(f"task_id={task.get('task_id')}")
    print(f"prompt_path={prompt_path}")
    shutil.rmtree(task_dir, ignore_errors=True)
    print("cleanup=removed queued smoke task")
    return 0


if __name__ == "__main__":
    sys.exit(main())
