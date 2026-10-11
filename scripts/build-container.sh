export WORKSPACE=/workspace/inference-eoap

command -v podman >/dev/null 2>&1 && { 

    podman build --format docker -t localhost/inference:latest -f ${WORKSPACE}/tile-based-classification/command-line-tools/inference/Dockerfile ${WORKSPACE}

} || command -v docker >/dev/null 2>&1 && { 

    docker build -t localhost/inference:latest -f ${WORKSPACE}/tile-based-classification/command-line-tools/inference/Dockerfile ${WORKSPACE}
}