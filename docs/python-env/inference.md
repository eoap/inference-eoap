### Goal

Run the command line tool in a Python virtual environment.

### Dependencies

This step depends on the execution of the `stage-and-cog.cwl` workflow that stages a Sentinel-2 Level-1C from the CDSE and converts/resamples its assets to COG.

### Lab

This step has a dedicated lab available at `/workspace/inference-eoap/practice-labs/Application steps/02 - Inference.ipynb`

### Step 1 - Configure the workspace

The results produced will be available in the local folder `/workspace/inference-eoap/runs`

```bash linenums="1" title="terminal"
--8<--
scripts/setup.sh
--8<--
```

### Step 2 - Create the Python virtual environment

The required Python modules are installed using `pip`:

```bash linenums="1" title="terminal"
--8<--
scripts/create_env.sh
--8<--
```


### Step 3 - Run the inference

The command line tool is invoked with:

```bash linenums="1" title="terminal"
--8<--
scripts/inference.sh
--8<--
```

### Step 4 - Clean-up

The Python virtual environment is no longer needed.

```bash linenums="1" title="terminal"
--8<--
scripts/deactivate.sh
--8<--
```

### Expected outcome

The folder `/workspace/inference-eoap/runs` contains: 

```
(base) jovyan@jupyter-mrossi--training:~/inference-eoap/runs$ tree .
.
├── S2B_10TFK_20210713_0_L2A
│   ├── S2B_10TFK_20210713_0_L2A.json
│   └── otsu.tif
├── catalog.json
└── otsu.tif

1 directory, 4 files
```