#!/bin/bash
# Run tests before commit
# Hook: PreToolUse (matcher: Bash) - checks if the command is a git commit
# Note: There is no "PreCommit" hook event. Use PreToolUse with a Bash matcher
# and inspect the command to detect git commit operations.
# A blocking hook must write its reason to stderr and exit 2. Exit 1 does not block.

INPUT=$(cat)

if command -v jq &> /dev/null; then
  COMMAND=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
elif command -v python3 &> /dev/null; then
  COMMAND=$(printf '%s' "$INPUT" | python3 -c '
import json
import sys

try:
    payload = json.load(sys.stdin)
except (json.JSONDecodeError, TypeError):
    payload = {}

tool_input = payload.get("tool_input", {}) if isinstance(payload, dict) else {}
command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
print(command if isinstance(command, str) else "")
' 2>/dev/null)
else
  exit 0
fi

# Tool matchers select Bash as a tool, not a specific shell command. Only run
# this hook when git's actual subcommand is commit (including git -C <path>).
if ! printf '%s\n' "$COMMAND" | grep -Eq '(^|&&|\|\||;)[[:space:]]*git(([[:space:]]+(--no-pager|--paginate|--literal-pathspecs))|([[:space:]]+(-C|-c|--git-dir|--work-tree)[[:space:]]+[^[:space:];&|]+))*[[:space:]]+commit([[:space:]]|$)'; then
  exit 0
fi

echo "🧪 Running tests before commit..."

# Check if package.json exists (Node.js project)
if [ -f "package.json" ]; then
  if grep -q "\"test\":" package.json; then
    if ! npm test; then
      echo "❌ Tests failed! Commit blocked." >&2
      exit 2
    fi
  fi
fi

# Check if pytest is available (Python project)
if [ -f "pytest.ini" ] || [ -f "setup.py" ]; then
  if command -v pytest &> /dev/null; then
    if ! pytest; then
      echo "❌ Tests failed! Commit blocked." >&2
      exit 2
    fi
  fi
fi

# Check if go.mod exists (Go project)
if [ -f "go.mod" ]; then
  if ! go test ./...; then
    echo "❌ Tests failed! Commit blocked." >&2
    exit 2
  fi
fi

# Check if Cargo.toml exists (Rust project)
if [ -f "Cargo.toml" ]; then
  if ! cargo test; then
    echo "❌ Tests failed! Commit blocked." >&2
    exit 2
  fi
fi

echo "✅ All tests passed! Proceeding with commit."
exit 0
