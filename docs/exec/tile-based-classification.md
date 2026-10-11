### Goal

Run the intended 2.0.0 workflow using `cwltool`. Source mode is the default during preparation; set `EOAP_ARTIFACT_MODE=release` and `EOAP_RELEASE_VERSION=<published-tag>` to validate matching release assets.

### Lab

This step has a dedicated lab available at `/workspace/inference-eoap/practice-labs/Execution-scenario.ipynb`

### Step 1 - Configure the workspace

The results produced will be available in the local folder `/workspace/inference-eoap/runs`

```bash linenums="1" title="terminal"
--8<--
scripts/setup.sh
--8<--
```

### Step 2 - Select the source or published Application Package

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