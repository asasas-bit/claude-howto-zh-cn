#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["pyyaml"]
# ///
"""Validate localization-sensitive files in the repository."""

from __future__ import annotations

import argparse
import json
import re
import subprocess  # nosec B404
import sys
from pathlib import Path

import yaml

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
ENGLISH_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z']{2,}\b")

MARKDOWN_IGNORE_PARTS = {
    ".git",
    ".pytest_cache",
    ".venv",
    "node_modules",
    "zh",
    "vi",
    "uk",
}

ALLOWED_ENGLISH_HEADING_RE = [
    re.compile(pattern)
    for pattern in [
        r"^#{1,6}\s+CLAUDE\.md$",
        r"^#{1,6}\s+v\d+\.\d+\.\d+\b.*$",
        r"^#{1,6}\s+CI/CD$",
        r"^#{1,6}\s+`[^`]+`$",
        r"^#{1,6}\s+/[A-Za-z0-9_-]+$",
    ]
]

ALLOWED_ENGLISH_HEADINGS_BY_PATH = {
    Path("README.md"): {
        "## Table of Contents",
        "## Contributing",
        "## License",
    }
}

FORBIDDEN_UNTRANSLATED_SNIPPETS = [
    "## Table of Contents",
    "## Contributing",
    "## License",
    "# Security Policy",
    "# Testing Guide",
    "# Publishing Notes",
    "## Review Template",
    "## Project Information",
    "## Executive Summary",
    "## Pre-Refactoring Checklist",
    "## Identified Code Smells",
    "## Refactoring Phases",
    "| Area | Status |",
    "| Feature Area | Score | Mastery | Status |",
    "This is a TypeScript web application.",
    "Run tests before commit.",
    "Keep API changes documented.",
]
LINK_VALIDATION_PATHS = [
    Path("README.md"),
    Path("UPSTREAM.md"),
    Path("LOCALIZATION-STYLE.md"),
    Path("LEARNING-ROADMAP.md"),
    Path("QUICK_REFERENCE.md"),
    Path("CATALOG.md"),
    Path("CHANGELOG.md"),
    Path("02-memory/README.md"),
    Path("03-skills/README.md"),
    Path("05-mcp/README.md"),
    Path("06-hooks/README.md"),
    Path("07-plugins/README.md"),
    Path("08-checkpoints/README.md"),
    Path("09-advanced-features/README.md"),
    Path("10-cli/README.md"),
    Path("scripts/README.md"),
    Path("01-slash-commands"),
    Path("03-skills/code-review-specialist/SKILL.md"),
    Path("04-subagents"),
]

PROTECTED_SNIPPETS = {
    Path("README.md"): [
        "## Table of Contents",
        "## Contributing",
        "## License",
        "UPSTREAM.md",
        "LOCALIZATION-STYLE.md",
    ],
    Path("01-slash-commands/pr.md"): [
        "allowed-tools:",
        "Bash(git add:*)",
        "Bash(git status:*)",
        "Bash(git diff:*)",
    ],
    Path("03-skills/code-review-specialist/SKILL.md"): [
        "name: code-review-specialist",
        "## 审查模板",
    ],
    Path("04-subagents/code-reviewer.md"): [
        "name: code-reviewer",
        "tools: Read, Grep, Glob, Bash",
        "model: inherit",
    ],
    Path("05-mcp/github-mcp.json"): [
        '"mcpServers"',
        '"github"',
        '"GITHUB_TOKEN"',
    ],
    Path("07-plugins/pr-review/.claude-plugin/plugin.json"): [
        '"name": "pr-review"',
        '"version"',
        '"license": "MIT"',
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def iter_link_validation_files(root: Path) -> list[Path]:
    files: set[Path] = set()
    for relative_path in LINK_VALIDATION_PATHS:
        path = root / relative_path
        if not path.exists():
            continue
        if path.is_file():
            files.add(path)
            continue
        files.update(child for child in path.rglob("*.md") if child.is_file())
    return sorted(files)


def validate_markdown_links(root: Path) -> list[str]:
    errors: list[str] = []
    for path in iter_link_validation_files(root):
        content = read_text(path)
        for raw_target in MARKDOWN_LINK_RE.findall(content):
            target = raw_target.strip()
            if not target or target.startswith("#"):
                continue
            if "://" in target or target.startswith(("mailto:", "javascript:")):
                continue
            target_path = target.split("#", 1)[0]
            resolved = (path.parent / target_path).resolve()
            if not resolved.exists():
                errors.append(f"{path}: broken relative link '{target}'")
    return errors


def split_frontmatter(content: str) -> str | None:
    if not content.startswith("---\n"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    return parts[1]


def validate_frontmatter(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*.md"):
        if ".venv" in path.parts or "node_modules" in path.parts:
            continue
        frontmatter = split_frontmatter(read_text(path))
        if frontmatter is None:
            continue
        try:
            loaded = yaml.safe_load(frontmatter)
        except yaml.YAMLError as exc:
            errors.append(f"{path}: invalid YAML frontmatter - {exc}")
            continue
        if loaded is not None and not isinstance(loaded, dict):
            errors.append(f"{path}: YAML frontmatter must parse to a mapping")
    return errors


def validate_data_files(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*.json"):
        if ".venv" in path.parts or "node_modules" in path.parts:
            continue
        try:
            json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON - {exc}")
    for suffix in ("*.yml", "*.yaml"):
        for path in root.rglob(suffix):
            if ".venv" in path.parts or "node_modules" in path.parts:
                continue
            try:
                yaml.safe_load(read_text(path))
            except yaml.YAMLError as exc:
                errors.append(f"{path}: invalid YAML - {exc}")
    return errors


def validate_shell_scripts(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*.sh"):
        if ".venv" in path.parts or "node_modules" in path.parts:
            continue
        # Validate repo-local shell files with `bash -n`.
        result = subprocess.run(  # nosec B603 B607
            ["bash", "-n", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            details = result.stderr.strip() or "bash -n failed"
            errors.append(f"{path}: invalid shell syntax - {details}")

    session_end = root / "06-hooks/session-end.sh"
    if session_end.is_file():
        executable_lines = [
            line.strip()
            for line in read_text(session_end).splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        if not executable_lines or executable_lines[-1] != "exit 0":
            errors.append(
                f"{session_end}: SessionEnd success exit must be the final command"
            )
    return errors


def iter_markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if not any(part in MARKDOWN_IGNORE_PARTS for part in path.parts)
    )


def is_allowed_english_heading(line: str) -> bool:
    return any(pattern.match(line) for pattern in ALLOWED_ENGLISH_HEADING_RE)


def strip_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


def looks_like_command_or_path(line: str) -> bool:
    stripped = line.strip()
    if stripped.startswith(("[![", "<", "|", "$", "# /", "# -", "- `", "* `")):
        return True
    command_prefixes = (
        "git ",
        "npm ",
        "npx ",
        "uv ",
        "python ",
        "python3 ",
        "bash ",
        "claude ",
        "curl ",
        "docker ",
        "kubectl ",
        "bq ",
        "cp ",
        "mkdir ",
    )
    return stripped.startswith(command_prefixes)


def validate_untranslated_english(root: Path) -> list[str]:
    errors: list[str] = []

    for path in iter_markdown_files(root):
        relative_path = path.relative_to(root)
        allowed_headings = ALLOWED_ENGLISH_HEADINGS_BY_PATH.get(relative_path, set())
        content = read_text(path)
        errors.extend(
            f"{path}: untranslated protected text '{snippet}'"
            for snippet in FORBIDDEN_UNTRANSLATED_SNIPPETS
            if snippet in content and snippet not in allowed_headings
        )

        in_fence = False
        in_frontmatter = False
        first_line = True
        for line_number, raw_line in enumerate(content.splitlines(), 1):
            line = raw_line.strip()
            if first_line and line == "---":
                in_frontmatter = True
                first_line = False
                continue
            first_line = False
            if in_frontmatter:
                if line == "---":
                    in_frontmatter = False
                continue
            if line.startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence or not line or looks_like_command_or_path(line):
                continue

            if line.startswith("#") and not CJK_RE.search(line):
                if line in allowed_headings:
                    continue
                if ENGLISH_WORD_RE.search(line) and not is_allowed_english_heading(
                    line
                ):
                    errors.append(
                        f"{path}:{line_number}: untranslated heading '{line}'"
                    )
                continue

            text = strip_inline_code(line)
            if CJK_RE.search(text):
                continue
            if len(ENGLISH_WORD_RE.findall(text)) >= 9:
                errors.append(
                    f"{path}:{line_number}: likely untranslated text '{line}'"
                )

    return errors


def validate_protected_snippets(root: Path) -> list[str]:
    errors: list[str] = []
    for relative_path, snippets in PROTECTED_SNIPPETS.items():
        path = root / relative_path
        if not path.exists():
            errors.append(f"{relative_path}: required file is missing")
            continue
        content = read_text(path)
        errors.extend(
            f"{relative_path}: missing protected snippet '{snippet}'"
            for snippet in snippets
            if snippet not in content
        )
    return errors


LESSON_DIRS = {
    f"{number:02d}": directory
    for number, directory in enumerate(
        (
            "01-slash-commands",
            "02-memory",
            "03-skills",
            "04-subagents",
            "05-mcp",
            "06-hooks",
            "07-plugins",
            "08-checkpoints",
            "09-advanced-features",
            "10-cli",
        ),
        1,
    )
}

V2_1_206_REQUIRED_SNIPPETS = {
    Path("01-slash-commands/README.md"): ["/dataviz", "${CLAUDE_PROJECT_DIR}"],
    Path("03-skills/README.md"): [
        "/dataviz",
        "${CLAUDE_PROJECT_DIR}",
        "叠加多个 skills",
        '"legacy-context": "name-only"',
        '"deploy": "off"',
    ],
    Path("04-subagents/README.md"): [
        "v2.1.198",
        "CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS",
        "--append-subagent-system-prompt",
    ],
    Path("05-mcp/README.md"): [
        "roots/list",
        "Pending approval",
        "enableAllProjectMcpServers",
    ],
    Path("06-hooks/README.md"): [
        "agent_needs_input",
        "agent_completed",
        "prompt_id",
    ],
    Path("07-plugins/README.md"): [
        "renames",
        "displayName",
        "defaultEnabled",
        "first-party-plugins",
        "healthcare",
    ],
    Path("08-checkpoints/README.md"): ["Summarize up to here"],
    Path("09-advanced-features/README.md"): [
        "`manual`",
        "askUserQuestionTimeout",
        "enableArtifact",
    ],
    Path("10-cli/README.md"): [
        "Org default",
        "--append-subagent-system-prompt",
        "CLAUDE_ENABLE_STREAM_WATCHDOG",
        "claude-sonnet-5",
    ],
}

V2_1_212_REQUIRED_SNIPPETS = {
    Path("claude_concepts_guide.md"): [
        "v2.1.212",
        "4 hops",
        "CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS",
    ],
    Path("resources.md"): [
        "claude auto-mode reset",
        "CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION",
        "--ax-screen-reader",
    ],
    Path("CATALOG.md"): [
        "2 套机制",
        "CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION",
        "--ax-screen-reader",
    ],
    Path("QUICK_REFERENCE.md"): [
        "claude auto-mode reset",
        "CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION",
        "CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS",
    ],
    Path("01-slash-commands/README.md"): [
        "/fork [prompt]",
        "/subtask <task>",
        "/branch [name]",
        "v2.1.212",
    ],
    Path("02-memory/README.md"): [
        "4 hops",
        "拼接",
        "managed-settings.d/",
        "命令行参数",
    ],
    Path("04-subagents/README.md"): [
        "v2.1.210",
        "CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION",
        "xhigh",
        "Task tool",
        "`mode`",
    ],
    Path("05-mcp/README.md"): ["CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS"],
    Path("09-advanced-features/README.md"): [
        "claude auto-mode reset",
        "--ax-screen-reader",
        "CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION",
        "disableAutoMode",
    ],
    Path("10-cli/README.md"): [
        "CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION",
        "CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION",
        "CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS",
        "CLAUDE_AX_SCREEN_READER",
    ],
}

V2_1_212_FORBIDDEN_SNIPPETS = {
    Path("02-memory/README.md"): ["当前教程按 8 层理解"],
    Path("09-advanced-features/README.md"): [
        "需要显式设置 `CLAUDE_CODE_ENABLE_AUTO_MODE=1`",
        "较新的主名称",
    ],
    Path("10-cli/README.md"): [
        "需要显式设置 `CLAUDE_CODE_ENABLE_AUTO_MODE=1`",
        "较新的主名称",
    ],
    Path("QUICK_REFERENCE.md"): ["某些版本中 `/fork` 仍可作为兼容别名"],
    Path("resources.md"): [
        "在 Bedrock / Vertex / Foundry 上对 Opus 4.7 / 4.8 显式启用"
    ],
    Path("CATALOG.md"): ["从当前对话分叉\uff08某些版本中 `/fork` 仍可能可用\uff09"],
}

V2_1_217_REQUIRED_SNIPPETS = {
    Path("UPSTREAM.md"): [
        "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS",
        "config-examples.json",
    ],
    Path("CHANGELOG.md"): ["v2.1.217", "8f04517", "97fc961"],
    Path("claude_concepts_guide.md"): [
        "v2.1.217",
        "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS",
        "sandbox.filesystem.disabled",
        "--permission-mode auto",
    ],
    Path("resources.md"): [
        "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS",
        "sandbox.filesystem.disabled",
    ],
    Path("CATALOG.md"): [
        "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH",
        "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS",
        "--permission-mode auto",
    ],
    Path("QUICK_REFERENCE.md"): [
        "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS",
        "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH",
        "--permission-mode auto",
    ],
    Path("01-slash-commands/README.md"): [
        "v2.1.216+` 起压缩失败",
        "context window 上限",
        "--permission-mode auto",
    ],
    Path("02-memory/README.md"): [
        "GUI editor",
        "`modified` 字段",
        "200 行以内",
    ],
    Path("03-skills/README.md"): [
        "v2.1.215+` 起只会在用户显式调用时运行",
    ],
    Path("03-skills/brand-voice/SKILL.md"): [
        "name: brand-voice",
        "user-invocable: false",
    ],
    Path("03-skills/claude-md/SKILL.md"): ["200 行以内"],
    Path("04-subagents/README.md"): [
        "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS",
        "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH",
    ],
    Path("06-hooks/README.md"): [
        "**/dir/**",
        '报告 `"fork"`',
        "deny / ask permission rules",
    ],
    Path("08-checkpoints/README.md"): ["symlink", "hard link", "跳过数量"],
    Path("09-advanced-features/README.md"): [
        "sandbox.filesystem.disabled",
        "emojiCompletionEnabled",
        "CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH",
    ],
    Path("09-advanced-features/config-examples.json"): [
        '"defaultMode"',
        '"fileCheckpointingEnabled"',
        '"PostToolUse"',
        '"claude-sonnet-5"',
    ],
    Path("10-cli/README.md"): [
        "--permission-mode auto",
        "--settings` 读取的文件",
        "10,000 字符",
        "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS",
        "CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH",
    ],
}

V2_1_217_FORBIDDEN_SNIPPETS = {
    Path("01-slash-commands/README.md"): [
        "不再强依赖 `--enable-auto-mode`",
    ],
    Path("03-skills/brand-voice/SKILL.md"): [
        "name: brand-voice-consistency",
    ],
    Path("03-skills/claude-md/SKILL.md"): ["目标尽量少于 300 行"],
    Path("04-subagents/README.md"): [
        "它可以继续 spawn 自己的子 subagent\uff0c最多嵌套 5 层",
    ],
    Path("CATALOG.md"): [
        "subagent 可以再 spawn 子 subagent\uff0c最多嵌套 5 层",
        "subagent 最多 5 层嵌套",
    ],
    Path("resources.md"): ["最多支持 5 层嵌套"],
    Path("claude_concepts_guide.md"): [
        "subagent 可以再 spawn 子 subagent\uff0c最多嵌套 5 层",
    ],
    Path("09-advanced-features/config-examples.json"): [
        '"planning"',
        '"extendedThinking"',
        '"headless"',
        '"autoCheckpoint"',
        '"mode": "unrestricted"',
        '"claude-opus-4-7"',
        '"PreToolUse:Write"',
    ],
}

V2_1_220_REQUIRED_SNIPPETS = {
    Path("README.md"): ["v2.1.220-r2", "b9a973b"],
    Path("UPSTREAM.md"): [
        "b9a973bf32bc28bdccb106012397e10235779bc3",
        "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1",
        "DirectoryAdded",
        "workflowSizeGuideline",
    ],
    Path("CHANGELOG.md"): ["v2.1.220", "97fc961", "343d6f0"],
    Path("INDEX.md"): ["v2.1.220", "默认深度为 3", "claude-opus-5"],
    Path("01-slash-commands/README.md"): [
        "/deep-research <topic>",
        "claude-opus-5",
        "Opus 5 和 Opus 4.8",
    ],
    Path("03-skills/README.md"): [
        "background: true",
        "background: false",
        "yes` / `no`",
        "/deep-research <topic>",
    ],
    Path("04-subagents/README.md"): [
        "默认深度为 3",
        "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1",
        "workspace trust",
        "不能包含 `:`",
    ],
    Path("05-mcp/README.md"): [
        "claude mcp list",
        "HTTP 状态与错误文本",
        "首尾空白字符",
        "mcp_server_errors",
    ],
    Path("06-hooks/README.md"): [
        "31 个 hook 事件、5 种 hook 类型",
        "DirectoryAdded",
        "register_repo_root",
        "workspace trust",
    ],
    Path("09-advanced-features/README.md"): [
        "permissions.disableAutoMode",
        "useAutoModeDuringPlan",
        "workflowSizeGuideline",
        "sandbox.network.strictAllowlist",
        "safety-classifier fallback",
    ],
    Path("10-cli/README.md"): [
        "claude-opus-5",
        "--forward-subagent-text",
        "workflowSizeGuideline",
        "默认 `3`\uff0c设为 `1`",
    ],
    Path("CATALOG.md"): [
        "31 个事件",
        "claude-opus-5",
        "mcp_server_errors",
        "workflowSizeGuideline",
    ],
    Path("QUICK_REFERENCE.md"): [
        "/deep-research topic",
        "默认深度 3",
        "--forward-subagent-text",
        "sandbox.network.strictAllowlist",
    ],
    Path("claude_concepts_guide.md"): [
        "v2.1.220",
        "mcp_server_errors",
        "31 个 hook 事件",
        "claude-opus-5",
    ],
    Path("resources.md"): [
        "claude-opus-5",
        "DirectoryAdded",
        "mcp_server_errors",
        "sandbox.network.strictAllowlist",
    ],
}

V2_1_220_FORBIDDEN_SNIPPETS = {
    Path("04-subagents/README.md"): [
        "subagent 嵌套现在默认关闭",
        "默认不设置\uff0c也就是不允许嵌套",
    ],
    Path("CATALOG.md"): [
        "从 `v2.1.217` 起嵌套默认关闭",
        "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` 显式开启嵌套",
        "Opus 4.8 默认 effort 是 `high`",
    ],
    Path("QUICK_REFERENCE.md"): ["显式开启 subagent 嵌套"],
    Path("resources.md"): [
        "`v2.1.217+` 默认关闭嵌套",
        "Vexilo",
    ],
    Path("claude_concepts_guide.md"): [
        "从 `v2.1.217` 起嵌套默认关闭",
    ],
    Path("06-hooks/README.md"): [
        "**30 个 hook 事件、5 种 hook 类型**",
    ],
    Path("09-advanced-features/README.md"): [
        "截至 `v2.1.217`\uff0cAuto Mode",
        "`v2.1.217+` 默认不允许嵌套",
        "核心变化是 **Opus 4.8**",
    ],
    Path("10-cli/README.md"): [
        "API 仍默认使用 Opus 4.8",
        "Opus 主线已经切到 **Opus 4.8**",
        "默认不允许嵌套",
        "让 Opus 4.6 走 fast mode",
    ],
}

V2_1_220_R2_REQUIRED_SNIPPETS = {
    Path("README.md"): ["v2.1.220-r2"],
    Path("UPSTREAM.md"): [
        "b9a973bf32bc28bdccb106012397e10235779bc3",
        "v2.1.220-r2",
    ],
    Path("CHANGELOG.md"): ["2026-08-05", "v2.1.220-r2", "b9a973b"],
    Path("INDEX.md"): ["v2.1.220-r2", "/fork", "/subtask"],
    Path("01-slash-commands/README.md"): [
        "/fewer-permission-prompts",
        "/fork [prompt]",
        "/subtask <task>",
        "/output-style",
        "outputStyle",
    ],
    Path("01-slash-commands/doc-refactor.md"): ["name: doc-refactor"],
    Path("01-slash-commands/setup-ci-cd.md"): ["name: setup-ci-cd"],
    Path("01-slash-commands/unit-test-expand.md"): ["name: unit-test-expand"],
    Path("02-memory/README.md"): [
        "autoMemoryEnabled",
        "CLAUDE_CODE_DISABLE_AUTO_MEMORY",
        "200 行以内",
        "AGENTS.md",
    ],
    Path("02-memory/directory-api-CLAUDE.md"): ["用于补充根目录"],
    Path("03-skills/README.md"): ["Enterprise > Project > Personal"],
    Path("03-skills/claude-md/SKILL.md"): ["AGENTS.md", "200 行以内"],
    Path("03-skills/refactor/SKILL.md"): ["name: refactor"],
    Path("04-subagents/README.md"): ["`color`", "`cyan`"],
    Path("05-mcp/README.md"): [
        "--scope local",
        "--scope project",
        "--scope user",
        "claude mcp add-json",
        "streamable-http",
    ],
    Path("05-mcp/database-mcp.json"): [
        '"type": "stdio"',
        '"DATABASE_URL": "${DATABASE_URL}"',
    ],
    Path("05-mcp/filesystem-mcp.json"): ['"type": "stdio"'],
    Path("05-mcp/github-mcp.json"): ['"type": "stdio"'],
    Path("05-mcp/multi-mcp.json"): ['"type": "stdio"'],
    Path("06-hooks/README.md"): [
        "`exit 2`",
        "`stderr`",
        "`defer`",
        "deny` > `defer` > `ask` > `allow",
    ],
    Path("06-hooks/dependency-check.sh"): [
        "INPUT=$(cat)",
        '"file_path"',
    ],
    Path("06-hooks/pre-commit.sh"): [
        ".tool_input.command",
        "git's actual subcommand is commit",
        "exit 2",
        ">&2",
    ],
    Path("06-hooks/session-end.sh"): ["exit 0"],
    Path("06-hooks/context-tracker.py"): ["CONTEXT_LIMIT = 1000000"],
    Path("06-hooks/context-tracker-tiktoken.py"): ["CONTEXT_LIMIT = 1000000"],
    Path("07-plugins/README.md"): [
        "anthropics/claude-plugins-community",
        "<plugin-name>@claude-community",
    ],
    Path("07-plugins/devops-automation/agents/alert-analyzer.md"): [
        "tools: Read, Grep, Bash"
    ],
    Path("07-plugins/devops-automation/agents/deployment-specialist.md"): [
        "tools: Read, Write, Bash, Grep"
    ],
    Path("07-plugins/devops-automation/agents/incident-commander.md"): [
        "tools: Read, Write, Bash, Grep"
    ],
    Path("07-plugins/documentation/agents/api-documenter.md"): [
        "tools: Read, Write, Grep"
    ],
    Path("07-plugins/documentation/agents/code-commentator.md"): [
        "tools: Read, Write, Edit"
    ],
    Path("07-plugins/documentation/agents/example-generator.md"): [
        "tools: Read, Write"
    ],
    Path("07-plugins/pr-review/agents/performance-analyzer.md"): [
        "tools: Read, Grep, Bash"
    ],
    Path("07-plugins/pr-review/agents/security-reviewer.md"): [
        "tools: Read, Grep, Bash"
    ],
    Path("07-plugins/pr-review/agents/test-checker.md"): ["tools: Read, Bash, Grep"],
    Path("08-checkpoints/README.md"): [
        "fileCheckpointingEnabled",
        "CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING",
        "100 个 checkpoints",
    ],
    Path("09-advanced-features/README.md"): [
        "permissions.defaultMode",
        "switchModelsOnFlag",
        "Output Styles",
        "Status Line",
        "outputStyle",
        "statusLine",
        "/subtask <task>",
    ],
    Path("09-advanced-features/config-examples.json"): [
        '"defaultMode": "manual"',
        '"model": "claude-opus-5"',
    ],
    Path("CATALOG.md"): [
        "/fewer-permission-prompts",
        "/subtask <task>",
        "11 | 适合自动化",
    ],
    Path("QUICK_REFERENCE.md"): [
        "/subtask 检查 flaky tests",
        "fileCheckpointingEnabled",
        "claude mcp add-json",
    ],
    Path("claude_concepts_guide.md"): [
        "/subtask <task>",
        "autoMemoryEnabled",
        "fileCheckpointingEnabled",
    ],
    Path("resources.md"): [
        "/fewer-permission-prompts",
        "anthropics/claude-plugins-community",
        "switchModelsOnFlag",
    ],
    Path("10-cli/README.md"): ["/fork [prompt]", "/subtask <task>"],
    Path("scripts/build_website.py"): [
        'REPO_URL = "https://github.com/lhfer/claude-howto-zh-cn"',
    ],
    Path("scripts/pyproject.toml"): [
        'include = ["**/*.py"]',
        '"PLR0917"',
    ],
    Path(".github/markdown-link-check-config.json"): [
        "https://github.com/lhfer/claude-howto-zh-cn/blob/main/",
        '"timeout": "10s"',
    ],
    Path(".github/ISSUE_TEMPLATE/config.yml"): [
        "Claude Code 官方文档",
        "查看 Anthropic 官方示例与实践",
    ],
}

V2_1_220_R2_FORBIDDEN_SNIPPETS = {
    Path("01-slash-commands/README.md"): [
        "/less-permission-prompts",
        "/fork <directive>",
    ],
    Path("01-slash-commands/doc-refactor.md"): [
        "name: Documentation Refactor",
        "tags:",
    ],
    Path("01-slash-commands/setup-ci-cd.md"): [
        "name: Setup CI/CD Pipeline",
        "tags:",
    ],
    Path("01-slash-commands/unit-test-expand.md"): [
        "name: Expand Unit Tests",
        "tags:",
    ],
    Path("02-memory/README.md"): ["控制在几百行内", "目录下的内容会覆盖"],
    Path("02-memory/directory-api-CLAUDE.md"): ["用于覆盖根目录"],
    Path("03-skills/README.md"): ["Enterprise > Personal > Project"],
    Path("03-skills/refactor/SKILL.md"): ["name: code-refactor"],
    Path("05-mcp/database-mcp.json"): [
        "postgresql://user:pass@localhost/mydb",
    ],
    Path("06-hooks/README.md"): ["成功返回 0\uff0c失败返回非 0"],
    Path("06-hooks/dependency-check.sh"): ["FILE=$1", "PostToolUse:Write"],
    Path("06-hooks/pre-commit.sh"): ["exit 1"],
    Path("06-hooks/context-tracker.py"): ["CONTEXT_LIMIT = 128000"],
    Path("06-hooks/context-tracker-tiktoken.py"): ["CONTEXT_LIMIT = 128000"],
    Path("09-advanced-features/README.md"): [
        "/fork <directive>",
        '"permissions": {"mode"',
    ],
    Path("09-advanced-features/config-examples.json"): [
        '"defaultMode": "default"',
        '"model": "claude-opus-4-8"',
    ],
    Path("CATALOG.md"): ["/less-permission-prompts", "/fork <directive>"],
    Path("QUICK_REFERENCE.md"): [
        "/fork 检查 flaky tests",
        "委派给继承完整对话的后台 subagent",
    ],
    Path("claude_concepts_guide.md"): ["/fork <directive>"],
    Path("resources.md"): ["/fork <directive>"],
    Path("10-cli/README.md"): ["/fork <directive>"],
    Path("scripts/build_website.py"): [
        'REPO_URL = "https://github.com/luongnv89/claude-howto"',
    ],
    Path("scripts/pyproject.toml"): ['include = ["scripts/**/*.py"]'],
    Path(".github/ISSUE_TEMPLATE/config.yml"): [
        "https://github.com/luongnv89/claude-howto/discussions",
    ],
}

V2_1_220_FOLLOWUP_REQUIRED_SNIPPETS = {
    Path("README.md"): ["2026-08-06", "b9a973b", "4f3fa85"],
    Path("UPSTREAM.md"): [
        "4f3fa85d7ed0f0f77f0d8bba3f0b40ff10b2063b",
        "Reviewed upstream range: `b9a973b` → `4f3fa85`",
        "--lang zh",
    ],
    Path("CHANGELOG.md"): ["2026-08-06", "b9a973b", "4f3fa85"],
    Path("INDEX.md"): ["4f3fa85", "本地 `mmdc`", "31 个 hook 事件"],
    Path("CLAUDE.md"): ["--lang zh", "EPUB 构建 jobs", "arm64"],
    Path("06-hooks/README.md"): [
        "`command`、`http`、`mcp_tool`、`prompt`、`agent`",
        "两者不是同一个分类轴",
    ],
    Path("scripts/build_epub.py"): [
        'mmdc_path: str = "mmdc"',
        '"--puppeteer-config"',
        "subprocess.run(",
        "mmdc produced no output",
    ],
    Path("scripts/README.md"): [
        "--mmdc-path",
        "--puppeteer-config",
        "EPUB 构建 jobs",
        "arm64",
    ],
    Path(".github/workflows/test.yml"): [
        "Install mmdc (Mermaid CLI)",
        "--lang zh",
        "if-no-files-found: error",
        "needs: [pytest, lint, security, type-check]",
        "codecov/codecov-action@v5",
    ],
    Path(".github/workflows/ci.yml"): [
        "Install mmdc (Mermaid CLI)",
        "--lang zh",
        "--puppeteer-config",
        "if-no-files-found: error",
        "codecov/codecov-action@v5",
    ],
    Path(".github/workflows/release.yml"): [
        "Install mmdc (Mermaid CLI)",
        "--lang zh",
        "--puppeteer-config",
        "test -s claude-howto-guide.epub",
    ],
    Path(".github/workflows/docs-check.yml"): [
        "actions/setup-python@v7",
        "node-version: '24'",
        "markdownlint-cli@0.49.1",
        "--config .markdownlint.json",
    ],
    Path(".pre-commit-config.yaml"): [
        "rev: v0.15.10",
        "args: [-c, scripts/pyproject.toml]",
        "markdownlint-cli@0.49.1",
        ".markdownlint.json",
    ],
    Path(".markdownlint.json"): ['"default": false', '"MD009": true'],
    Path("scripts/pyproject.toml"): [
        'include = ["**/*.py"]',
        '"tests/*.py"',
        '"PLR0917"',
        "[tool.mypy]",
        "ignore_missing_imports = true",
    ],
    Path("scripts/requirements-dev.txt"): ["ruff>=0.15.10", "mypy>=1.8.0"],
    Path(".cspell.json"): ['"httpx"'],
}

V2_1_220_FOLLOWUP_FORBIDDEN_SNIPPETS = {
    Path("scripts/build_epub.py"): [
        "Kroki.io",
        "import httpx",
        "from tenacity",
        '"--timeout"',
        '"--max-concurrent"',
    ],
    Path("scripts/README.md"): ["Kroki.io", "--timeout", "--max-concurrent"],
    Path("scripts/requirements.txt"): ["httpx", "tenacity"],
    Path("scripts/pyproject.toml"): [
        '"httpx"',
        '"tenacity"',
        '"scripts/tests/*.py"',
        '"B113"',
    ],
    Path(".cspell.json"): ['"tenacity"'],
    Path(".pre-commit-config.yaml"): [
        "rev: v0.8.2",
        "args: [-c, pyproject.toml]",
    ],
    Path(".github/workflows/test.yml"): [
        "continue-on-error: true",
        "codecov/codecov-action@v3",
    ],
    Path(".github/workflows/ci.yml"): ["codecov/codecov-action@v3"],
    Path(".github/workflows/docs-check.yml"): [
        "actions/setup-python@v4",
        "continue-on-error: true",
        "node-version: '18'",
    ],
}


def normalize_heading(value: str) -> str:
    return re.sub(r"[`*_]", "", value).strip().casefold()


def validate_curriculum_consistency(root: Path) -> list[str]:  # noqa: PLR0912
    """Check cross-document facts that syntax and link checks cannot catch."""

    errors: list[str] = []
    required_paths = [
        Path(".claude/skills/lesson-quiz/SKILL.md"),
        Path(".claude/skills/lesson-quiz/references/question-bank.md"),
        Path(".claude/skills/lesson-quiz/references/results-template.md"),
        Path(".claude/skills/self-assessment/SKILL.md"),
        Path(".claude/skills/self-assessment/references/deep-assessment-rounds.md"),
        Path(".claude/skills/self-assessment/references/output-templates.md"),
        Path(".claude/skills/self-assessment/references/topic-recommendations.md"),
        Path("06-hooks/README.md"),
    ]
    missing = [path for path in required_paths if not (root / path).is_file()]
    if missing:
        return [f"{path}: required curriculum file is missing" for path in missing]

    lesson_skill_path = root / required_paths[0]
    question_bank_path = root / required_paths[1]
    results_template_path = root / required_paths[2]
    assessment_skill_path = root / required_paths[3]
    deep_rounds_path = root / required_paths[4]
    assessment_template_path = root / required_paths[5]
    topic_recommendations_path = root / required_paths[6]
    hooks_path = root / required_paths[7]

    lesson_skill = read_text(lesson_skill_path)
    question_bank = read_text(question_bank_path)
    results_template = read_text(results_template_path)
    assessment_skill = read_text(assessment_skill_path)
    deep_rounds = read_text(deep_rounds_path)
    assessment_template = read_text(assessment_template_path)
    topic_recommendations = read_text(topic_recommendations_path)
    hooks = read_text(hooks_path)

    if (
        "每轮 2 题，共 5 轮" not in lesson_skill  # noqa: RUF001
        or "所有 4 轮" in lesson_skill
    ):
        errors.append(
            f"{lesson_skill_path}: lesson quiz must consistently use 5 rounds"
        )

    frontmatter = split_frontmatter(lesson_skill)
    loaded = yaml.safe_load(frontmatter) if frontmatter else {}
    metadata = loaded.get("metadata", {}) if isinstance(loaded, dict) else {}
    if not isinstance(metadata, dict) or metadata.get("version") != "1.1.0":
        errors.append(
            f"{lesson_skill_path}: version 1.1.0 must be stored as metadata.version"
        )
    if isinstance(loaded, dict) and "version" in loaded:
        errors.append(f"{lesson_skill_path}: top-level version key is stale")
    raw_description = loaded.get("description", "") if isinstance(loaded, dict) else ""
    description = raw_description if isinstance(raw_description, str) else ""
    if "整套教程" not in description or "解释" not in description:
        errors.append(
            f"{lesson_skill_path}: description must include negative trigger boundaries"
        )

    lesson_questions: dict[str, list[dict[str, str]]] = {}
    current_lesson = ""
    current_question: dict[str, str] | None = None
    for line in question_bank.splitlines():
        lesson_match = re.match(r"^## Lesson (\d{2})", line)
        if lesson_match:
            current_lesson = lesson_match.group(1)
            lesson_questions[current_lesson] = []
            current_question = None
            continue
        question_match = re.match(r"^### Q(\d+)$", line)
        if question_match and current_lesson:
            current_question = {"number": question_match.group(1)}
            lesson_questions[current_lesson].append(current_question)
            continue
        if current_question is None:
            continue
        field_match = re.match(r"^- \*\*(Category|Correct|Review)\*\*: (.+)$", line)
        if field_match:
            current_question[field_match.group(1).lower()] = field_match.group(2)
        if line.startswith("- **Options**: "):
            current_question["options"] = line.removeprefix("- **Options**: ")
        if line.startswith("- **Explanation**: "):
            current_question["explanation"] = line.removeprefix("- **Explanation**: ")

    for lesson_number, lesson_dir in LESSON_DIRS.items():
        questions = lesson_questions.get(lesson_number, [])
        if [item.get("number") for item in questions] != [str(i) for i in range(1, 11)]:
            errors.append(
                f"{question_bank_path}: lesson {lesson_number} must contain Q1-Q10"
            )
            continue
        categories = [item.get("category") for item in questions]
        if categories.count("conceptual") != 5 or categories.count("practical") != 5:
            errors.append(
                f"{question_bank_path}: lesson {lesson_number} must have 5 conceptual and 5 practical questions"
            )

        lesson_readme = root / lesson_dir / "README.md"
        if not lesson_readme.is_file():
            errors.append(f"{lesson_readme}: required lesson README is missing")
            continue
        headings = {
            normalize_heading(match.group(1))
            for line in read_text(lesson_readme).splitlines()
            if (match := re.match(r"^#{2,6}\s+(.+)$", line))
        }
        for question in questions[8:10]:
            review = question.get("review", "")
            if normalize_heading(review) not in headings:
                errors.append(
                    f"{question_bank_path}: lesson {lesson_number} Q{question.get('number')} review pointer '{review}' does not match a localized heading"
                )

    hook_summary = re.search(r"\*\*(\d+) 个 hook 事件、(\d+) 种 hook 类型\*\*", hooks)
    if not hook_summary:
        errors.append(f"{hooks_path}: missing hook event/type summary")
    else:
        event_count, type_count = map(int, hook_summary.groups())
        hook_questions = lesson_questions.get("06", [])
        if len(hook_questions) < 9:
            errors.append(f"{question_bank_path}: Hooks Q9 is missing")
            hook_q9: dict[str, str] = {}
        else:
            hook_q9 = hook_questions[8]
        option_values = {
            letter: int(value)
            for letter, value in re.findall(
                r"([A-D])\)\s*(\d+)", hook_q9.get("options", "")
            )
        }
        correct = hook_q9.get("correct", "")
        if option_values.get(correct) != event_count:
            errors.append(
                f"{question_bank_path}: Hooks Q9 correct answer must match {event_count} events"
            )
        if f"{event_count} 个 hook 事件" not in hook_q9.get("explanation", ""):
            errors.append(
                f"{question_bank_path}: Hooks Q9 explanation must use {event_count} events"
            )
        if (
            f"{event_count} 个 hook 事件" not in topic_recommendations
            or f"{type_count} 种 hook 类型" not in topic_recommendations
        ):
            errors.append(
                f"{topic_recommendations_path}: hook recommendation must match {event_count} events and {type_count} types"
            )

    english_output_fragments = (
        "Lesson Quiz Results:",
        "Quiz timing",
        "Question breakdown",
        "Incorrect Answers — Review These",
        "Your answer:",
        "Correct answer:",
        "Pre-test score:",
        "Progress check:",
        "Mastery check:",
        "Recommended Next Steps",
        "Would you like to retake this quiz",
        "[next lesson link]",
        "[list sections]",
    )
    errors.extend(
        f"{results_template_path}: untranslated user-facing text '{fragment}'"
        for fragment in english_output_fragments
        if fragment in results_template
    )

    if "N/20" in assessment_skill or "N/20" in assessment_template:
        errors.append(f"{assessment_skill_path}: Deep Assessment maximum is 19, not 20")
    if "N/19" not in assessment_skill or "N/19" not in assessment_template:
        errors.append(
            f"{assessment_template_path}: Deep Assessment output must use N/19"
        )
    if "8 个问题" in assessment_skill:
        errors.append(
            f"{assessment_skill_path}: Quick Assessment has 8 items across 2 questions"
        )
    if (
        "每轮覆盖 2 个能力域，每个能力域对应 2 个选项"  # noqa: RUF001
        in deep_rounds
    ):
        errors.append(f"{deep_rounds_path}: round 4 uses a 1/3 option split, not 2/2")

    untranslated_assessment_fragments = (
        "Which of these have you done? Select all that apply.",
        "Created a custom slash command or skill",
        "Installed and used an auto-invoked skill",
        "Connected an MCP server and used its tools",
        "Used checkpoints for safe experimentation",
        "Installed or created a plugin",
        "- Tutorial:",
        "- Focus on:",
        "- Key exercise:",
        "- Done when:",
    )
    for path, content in (
        (deep_rounds_path, deep_rounds),
        (topic_recommendations_path, topic_recommendations),
    ):
        errors.extend(
            f"{path}: untranslated assessment text '{fragment}'"
            for fragment in untranslated_assessment_fragments
            if fragment in content
        )
    if "2% context budget" in topic_recommendations:
        errors.append(
            f"{topic_recommendations_path}: skill description budget must be 1%"
        )

    for version, required_snippets in (
        ("v2.1.206", V2_1_206_REQUIRED_SNIPPETS),
        ("v2.1.212", V2_1_212_REQUIRED_SNIPPETS),
        ("v2.1.217", V2_1_217_REQUIRED_SNIPPETS),
        ("v2.1.220", V2_1_220_REQUIRED_SNIPPETS),
        ("v2.1.220-r2", V2_1_220_R2_REQUIRED_SNIPPETS),
        ("v2.1.220-followup", V2_1_220_FOLLOWUP_REQUIRED_SNIPPETS),
    ):
        for relative_path, snippets in required_snippets.items():
            path = root / relative_path
            if not path.is_file():
                errors.append(
                    f"{relative_path}: required {version} document is missing"
                )
                continue
            content = read_text(path)
            errors.extend(
                f"{relative_path}: missing {version} content '{snippet}'"
                for snippet in snippets
                if snippet not in content
            )

    for relative_path, snippets in V2_1_212_FORBIDDEN_SNIPPETS.items():
        path = root / relative_path
        if not path.is_file():
            continue
        content = read_text(path)
        errors.extend(
            f"{relative_path}: stale v2.1.212 content '{snippet}'"
            for snippet in snippets
            if snippet in content
        )

    for relative_path, snippets in V2_1_217_FORBIDDEN_SNIPPETS.items():
        path = root / relative_path
        if not path.is_file():
            continue
        content = read_text(path)
        errors.extend(
            f"{relative_path}: stale v2.1.217 content '{snippet}'"
            for snippet in snippets
            if snippet in content
        )

    for relative_path, snippets in V2_1_220_FORBIDDEN_SNIPPETS.items():
        path = root / relative_path
        if not path.is_file():
            continue
        content = read_text(path)
        errors.extend(
            f"{relative_path}: stale v2.1.220 content '{snippet}'"
            for snippet in snippets
            if snippet in content
        )

    for relative_path, snippets in V2_1_220_R2_FORBIDDEN_SNIPPETS.items():
        path = root / relative_path
        if not path.is_file():
            continue
        content = read_text(path)
        errors.extend(
            f"{relative_path}: stale v2.1.220-r2 content '{snippet}'"
            for snippet in snippets
            if snippet in content
        )

    for relative_path, snippets in V2_1_220_FOLLOWUP_FORBIDDEN_SNIPPETS.items():
        path = root / relative_path
        if not path.is_file():
            continue
        content = read_text(path)
        errors.extend(
            f"{relative_path}: stale v2.1.220 follow-up content '{snippet}'"
            for snippet in snippets
            if snippet in content
        )

    return errors


def validate_root(root: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_markdown_links(root))
    errors.extend(validate_frontmatter(root))
    errors.extend(validate_data_files(root))
    errors.extend(validate_shell_scripts(root))
    errors.extend(validate_untranslated_english(root))
    errors.extend(validate_protected_snippets(root))
    errors.extend(validate_curriculum_consistency(root))
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate localization-sensitive content in the repository."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root to validate.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors = validate_root(root)
    if errors:
        print("Localization validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Localization validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
