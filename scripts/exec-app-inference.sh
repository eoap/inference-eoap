version="1.0.0"

export WORKSPACE=/workspace/inference-eoap

# check if the results.json file exists
if [ ! -f ${WORKSPACE}/runs/results.json ]; then
    echo "results.json file not found, run the stage-and-cog.cwl workflow first."
    exit 1
fi

cwltool \
    --podman \
    --outdir ${WORKSPACE}/runs \
    ${WORKSPACE}/runs/tile-based-classification.${version}.cwl \
    --input-item $( cat ${WORKSPACE}/runs/results.json | jq .stac_catalog.path )