#!/bin/sh
# tiny_repo_setup.sh — optional helper: create a minimal git repo + brief for
# manual (non-automated) smoke testing of audit-council scripts.
#
# Usage: tiny_repo_setup.sh <target-dir>
set -eu
DIR="${1:?usage: tiny_repo_setup.sh <target-dir>}"
mkdir -p "$DIR/src"
cd "$DIR"
git init -q
git config user.email t@example.com
git config user.name tester
cat > src/app.py <<'EOF'
def divide(a, b):
    return a / b  # no zero check: intentional audit target
EOF
cat > audit-brief.md <<'EOF'
# Audit brief
Verify the arithmetic helpers in src/app.py handle all documented inputs.
EOF
git add -A
git commit -qm "tiny repo"
echo "tiny repo ready: $DIR"
