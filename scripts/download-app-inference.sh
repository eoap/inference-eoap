version="1.0.0"

export WORKSPACE=/workspace/inference-eoap

wget \
    -O ${WORKSPACE}/runs/tile-based-classification.${version}.cwl \
    https://github.com/eoap/inference-eoap/releases/download/1.0.0/tile-based-classification.${version}.cwl