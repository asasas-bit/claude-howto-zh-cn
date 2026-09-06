"""Regression tests for the git commit gate hook."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK_SCRIPT = REPO_ROOT / "06-hooks" / "pre-commit.sh"


def run_hook(
    command: str, project_dir: Path, *, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    hook_env = {**os.environ, **(env or {})}
    return subprocess.run(
        ["bash", str(HOOK_SCRIPT)],
        cwd=project_dir,
        input=payload,
        text=True,
        capture_output=True,
        env=hook_env,
        check=False,
    )


@pytest.mark.parametrize(
    "command",
    ["git status", "git show commit", "echo git commit", "npm test"],
)
def test_non_commit_commands_skip_tests(command: str, tmp_path: Path) -> None:
    result = run_hook(command, tmp_path)

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_git_commit_command_runs_gate(tmp_path: Path) -> None:
    result = run_hook("git -C . commit -m docs", tmp_path)

    assert result.returncode == 0
    assert "Running tests before commit" in result.stdout
    assert "All tests passed" in result.stdout


def test_failed_tests_block_commit_with_stderr_reason(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(
        '{"scripts":{"test":"exit 1"}}', encoding="utf-8"
    )
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    npm = bin_dir / "npm"
    npm.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    npm.chmod(0o755)

    result = run_hook(
        "git commit -m docs",
        tmp_path,
        env={"PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"},
    )

    assert result.returncode == 2
    assert "Commit blocked" in result.stderr
