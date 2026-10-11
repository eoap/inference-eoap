#!/usr/bin/env bash
set -euo pipefail
export WORKSPACE=${WORKSPACE:-/workspace/inference-eoap}
mkdir -p "$WORKSPACE/runs"
CDSE_ACCESS_TOKEN=""
if [ -z "${CDSE_S3_ACCESS_KEY:-}" ]; then CDSE_ACCESS_TOKEN=$(get-bearer-token); fi
export CDSE_ACCESS_TOKEN
params=$(mktemp)
trap 'rm -f "$params"' EXIT
python - "$params" <<'PARAMS'
import json, os, sys
with open(sys.argv[1], 'w') as stream:
    json.dump({'access_token': os.environ['CDSE_ACCESS_TOKEN'], 'item': {'value': 'https://stac.dataspace.copernicus.eu/v1/collections/sentinel-2-l1c/items/S2A_MSIL1C_20240125T100311_N0510_R122_T33TVM_20240125T104959'}}, stream)
PARAMS
cwltool --podman --custom-net host --preserve-environment CDSE_S3_ACCESS_KEY --preserve-environment CDSE_S3_SECRET_KEY --outdir "$WORKSPACE/runs/staged" "$WORKSPACE/cwl-workflow/stage-and-cog.cwl" "$params" > "$WORKSPACE/runs/results.json"
