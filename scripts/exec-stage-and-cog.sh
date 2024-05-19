version="1.0.0"

export WORKSPACE=/workspace/inference-eoap

export PATH=${WORKSPACE}/bin:$PATH

read -p "Enter the CDSE username: " username
read -sp "Enter the CDSE password: " password

BEARER_TOKEN=$( get-bearer-token ${username} ${password} )
    
cwltool \
    --podman \
    --outdir ${WORKSPACE}/runs \
    https://github.com/eoap/inference-eoap/releases/download/1.0.0/stage-and-cog.1.0.0.cwl \
    --access_token ${BEARER_TOKEN} \
    --item "https://catalogue.dataspace.copernicus.eu/stac/collections/SENTINEL-2/items/S2A_MSIL1C_20240125T100311_N0510_R122_T33TVM_20240125T104959.SAFE" > ${WORKSPACE}/runs/results.json