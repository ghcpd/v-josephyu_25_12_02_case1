#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN=${PYTHON:-python3}
VENV_DIR=${VENV_DIR:-.venv}

if [[ ! -d "$VENV_DIR" ]]; then
  echo "[setup] Creating virtualenv at $VENV_DIR"
  "$PYTHON_BIN" -m venv "$VENV_DIR"
else
  echo "[setup] Reusing existing virtualenv at $VENV_DIR"
fi

VENV_PY="$VENV_DIR/bin/python"

"$VENV_PY" -m pip install --upgrade pip
"$VENV_PY" -m pip install -r requirements.txt

echo "✅ Environment ready. Activate with: source $VENV_DIR/bin/activate"
