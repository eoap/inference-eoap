WORKSPACE=/workspace/inference-eoap
RUNTIME=${WORKSPACE}/runs
mkdir -p ${RUNTIME}
cd ${RUNTIME}

# check if the results.json file exists
if [ ! -f ${WORKSPACE}/results.json ]; then
    echo "results.json file not found, run the stage-and-cog.cwl workflow first."
    exit 1
fi

python \
    ${WORKSPACE}/tile-based-classification/command-line-tools/inference/app.py \
    --input-item $( cat ${WORKSPACE}/results.json | jq .stac_catalog.path )