export WORKSPACE=/workspace/inference-eoap

command -v podman >/dev/null 2>&1 && { 
    flag="--podman"
}

cwltool ${flag} \
    --outdir ${WORKSPACE}/runs \
    ${WORKSPACE}/cwl-cli/inference.cwl \
    TODO