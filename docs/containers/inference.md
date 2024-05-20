### Goal 

* Build the container image
* Run the tile based classification inference in the container image tagged `localhost/inference:latest`.

### Lab

This step has a dedicated lab available at `/workspace/inference-eoap/practice-labs/Container.ipynb`

### The container recipe

The  tile based classification inference has a recipe to build the container image.

The `inference` step container image recipe is:

```dockerfile linenums="1" title="inference/Dockerfile"
--8<--
inference-eoap/tile-based-classification/command-line-tools/inference/Dockerfile
--8<--
```

### Building the container

Build the container images with:

```bash linenums="1" title="terminal"
--8<--
scripts/build-container.sh
--8<--
```

### Expected outcome

The local container registry lists the built images:

```
(base) jovyan@coder-mrossi:~/runs$ podman images | grep localhost
localhost/inference  latest      534f3f10c06e  11 minutes ago  530 MB
```

### How to run a step in a container

We'll use `podman` container engine (`docker` is also fine).

The command to run the `inference` step in the container is:

```bash linenums="1"
--8<--
scripts/podman-inference.sh
--8<--
```

Let's break down what this command does:

* `podman run`: This is the command to run a container.
* `-i`: This flag makes the container interactive, allowing you to interact with it via the terminal.
* `--userns=keep-id`: It instructs `podman` to keep the user namespace ID.
* `--mount=type=bind,source=/workspace/runs,target=/runs`: This option mounts a directory from the host system to the container. In this case, it mounts the `/workspace/runs` directory on the host to the /runs directory inside the container.
* `--workdir=/runs`: Sets the working directory inside the container to `/runs`.
* `--read-only=true`: Makes the file system inside the container read-only, meaning you can't write or modify files inside the container.
* `--user=1001:100`: Specifies the user and group IDs to be used within the container.
* `--rm`: This flag tells podman to remove the container after it has finished running.
* `--env=HOME=/runs`: Sets the `HOME` environment variable inside the container to `/runs`.
* `--env=PYTHONPATH=/app`: Sets the `PYTHONPATH` environment variable inside the container to `/app`.
* `localhost/inference:latest`: This is the name of the container image that you want to run. It's pulling the image from the local container registry with the name "inference" and the "latest" tag.
* `python -m app`: This is the command to run inside the container. It runs a Python module named "app".
* `--input-item ...`: Specifies the path to the folder where there is a `catalog.json` file.

### Expected outcome

The folder `/workspace/inference-eoap/runs` contains: 

```
(base) jovyan@jupyter-mrossi--training:~/inference-eoap$ tree runs/
runs
├── S2A_T33TVM_20240125T100359_L1C-classification
│   ├── S2A_T33TVM_20240125T100359_L1C-classification.json
│   └── classification.tif
├── catalog.json
├── results.json
└── ydmns4od
    ├── S2A_T33TVM_20240125T100359_L1C
    │   ├── S2A_T33TVM_20240125T100359_L1C.json
    │   ├── blue.tif
    │   ├── cirrus.tif
    │   ├── coastal.tif
    │   ├── green.tif
    │   ├── nir.tif
    │   ├── nir08.tif
    │   ├── nir09.tif
    │   ├── red.tif
    │   ├── rededge1.tif
    │   ├── rededge2.tif
    │   ├── rededge3.tif
    │   ├── swir16.tif
    │   └── swir22.tif
    └── catalog.json

3 directories, 19 files
```
