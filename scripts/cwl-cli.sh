export WORKSPACE=/workspace/inference-eoap

# check if the results.json file exists
if [ ! -f ${WORKSPACE}/runs/results.json ]; then
    echo "results.json file not found, run the stage-and-cog.cwl workflow first."
    exit 1
fi

command -v podman >/dev/null 2>&1 && { 
    flag="--podman"
}

cwltool ${flag} \
    --outdir ${WORKSPACE}/runs \
    ${WORKSPACE}/cwl-cli/inference.cwl \
    $( cat ${WORKSPACE}/runs/results.json | jq -r .stac_catalog.path )