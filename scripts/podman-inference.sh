WORKSPACE=/workspace/inference-eoap
RUNTIME=${WORKSPACE}/runs
mkdir -p ${RUNTIME}
cd ${RUNTIME}

# check if the results.json file exists
if [ ! -f ${WORKSPACE}/runs/results.json ]; then
    echo "results.json file not found, run the stage-and-cog.cwl workflow first."
    exit 1
fi

podman run \
    -i \
    --userns=keep-id \
    --mount=type=bind,source=/workspace/inference-eoap/runs,target=/runs \
    --workdir=/runs \
    --read-only=true \
    --user=1001:100 \
    --rm \
    --env=HOME=/runs \
    --env=PYTHONPATH=/app \
    localhost/inference:latest \
    python \
    -m \
    app \
    --input-item \
    $( cat ${WORKSPACE}/runs/results.json | jq -r .stac_catalog.path )