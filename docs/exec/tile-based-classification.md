### Goal

Run the `tile-based-classification.1.0.0.cwl` released application package using `cwltool`.

### Lab

This step has a dedicated lab available at `/workspace/inference-eoap/practice-labs/Execution-scenario.ipynb`

### Step 1 - Configure the workspace

The results produced will be available in the local folder `/workspace/inference-eoap/runs`

```bash linenums="1" title="terminal"
--8<--
scripts/setup.sh
--8<--
```

### Step 2 - Download the released Application package

```bash linenums="1" title="scripts/download-app-inference.sh"
--8<--
scripts/download-app-inference.sh
--8<--
```

### Step 3 - Execute the Application Package

```bash linenums="1" title="scripts/exec-app-inference.sh"
--8<--
scripts/exec-app-inference.sh
--8<--
```

### Expected outcome

The folder `/workspace/inference-eoap/runs` contains: 

``` hl_lines="3"
(base) jovyan@jupyter-fbrito--training:~/inference-eoap$ tree runs
runs
TODO
2 directories, 5 files
```