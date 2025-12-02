#!/usr/bin/env bash
set -euo pipefail
VENV_PY="${VENV_PY:-.venv/bin/python}"

if [[ ! -x "$VENV_PY" ]]; then
  echo "Error: $VENV_PY not found. Run ./setup.sh first." >&2
  exit 1
fi

"$VENV_PY" -m pytest test_files "$@"
