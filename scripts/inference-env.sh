#!/usr/bin/env bash
set -euo pipefail
export WORKSPACE=${WORKSPACE:-/workspace/inference-eoap}
uv venv --seed --python "${EOAP_PYTHON:-python3.12}" "$WORKSPACE/env_inference"
source "$WORKSPACE/env_inference/bin/activate"
uv pip sync --require-hashes "$WORKSPACE/requirements-runtime.txt"
