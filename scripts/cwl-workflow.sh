export WORKSPACE=/workspace/inference-eoap

command -v podman >/dev/null 2>&1 && { 
    flag="--podman"
}

# check if the results.json file exists
if [ ! -f ${WORKSPACE}/results.json ]; then
    echo "results.json file not found, run the stage-and-cog.cwl workflow first."
    exit 1
fi


cwltool ${flag} \
    --outdir ${WORKSPACE}/runs \
    ${WORKSPACE}/cwl-workflow/tile-based-classification.cwl.cwl \
    --input-item $( cat ${WORKSPACE}/runs/results.json | jq .stac_catalog.path )