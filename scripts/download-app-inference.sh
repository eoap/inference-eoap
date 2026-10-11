#!/usr/bin/env bash
set -euo pipefail
export WORKSPACE=${WORKSPACE:-/workspace/inference-eoap}
version=${EOAP_RELEASE_VERSION:-2.0.0}
mkdir -p "$WORKSPACE/runs"
if [ "${EOAP_ARTIFACT_MODE:-source}" = source ]; then
    cp "$WORKSPACE/cwl-workflow/tile-based-classification.cwl" "$WORKSPACE/runs/tile-based-classification.$version.cwl"
else
    curl --fail --location --output "$WORKSPACE/runs/tile-based-classification.$version.cwl" "https://github.com/eoap/inference-eoap/releases/download/$version/tile-based-classification.$version.cwl"
fi
