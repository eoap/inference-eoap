#!/usr/bin/env bash
set -euo pipefail
export WORKSPACE=${WORKSPACE:-/workspace/inference-eoap}
uv venv --allow-existing --seed --python "${EOAP_PYTHON:-python3.12}" "$WORKSPACE/env_stage_in"
source "$WORKSPACE/env_stage_in/bin/activate"
uv pip sync --require-hashes "$WORKSPACE/requirements-runtime.txt"
