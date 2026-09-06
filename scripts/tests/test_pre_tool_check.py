"""Regression tests for the pre-tool safety hook."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK_SCRIPT = REPO_ROOT / "06-hooks" / "pre-tool-check.sh"


def run_hook(command: str, project_dir: Path) -> subprocess.CompletedProcess[str]:
    payload = json.dumps(
        {"tool_name": "Bash", "tool_input": {"command": command}},
        ensure_ascii=False,
    )
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(project_dir)}
    return subprocess.run(
        ["bash", str(HOOK_SCRIPT)],
        input=payload,
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )


def test_block_reason_is_reported_on_stderr_and_audited(tmp_path: Path) -> None:
    result = run_hook("rm -rf /", tmp_path)

    assert result.returncode == 2
    assert result.stdout == ""
    assert "Blocked" in result.stderr

    audit_log = tmp_path / ".claude" / "hooks" / "audit.log"
    assert audit_log.exists()
    assert "BLOCK:" in audit_log.read_text(encoding="utf-8")


def test_rm_rf_tmp_path_warns_but_is_not_falsely_blocked(tmp_path: Path) -> None:
    result = run_hook("rm -rf /tmp/project", tmp_path)

    assert result.returncode == 0
    assert result.stdout == ""
    assert "Warning" in result.stderr
    assert "Blocked" not in result.stderr

    audit_log = tmp_path / ".claude" / "hooks" / "audit.log"
    assert audit_log.exists()
    log_content = audit_log.read_text(encoding="utf-8")
    assert "WARN:" in log_content
    assert "rm -rf /tmp/project" in log_content
