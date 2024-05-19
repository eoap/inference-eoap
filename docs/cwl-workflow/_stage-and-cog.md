### Goal

Run the _stage-and-cog.cwl_ CWL Workflow that that stages a Sentinel-2 Level-1C from the CDSE and converts/resamples its assets to COG.

### Dependencies

This steps requires generating a CDSE access token with the Python script and your own CDSE credentials: 

```python linenums="1" title="bin/get-bearer-token"
--8<--
bin/get-bearer-token
--8<--
```

### Lab

This step has a dedicated lab available at `/workspace/inference-eoap/practice-labs/Application steps/01 - Stage-and-cog.ipynb`

### Step 1 - Run the stage-and-cog.cwl_ CWL Workflow 

Use `cwltool` to run the _stage-and-cog.cwl_ CWL Workflow with a Sentinel-2 Level-1C acquisition reference

The CWL Workflow is shown below and the lines highlighted chain the `stage-in` and `conversion` to COG steps:

```yaml linenums="1" title="stage-and-cog.cwl"
--8<--
cwl-workflow/stage-and-cog.cwl
--8<--
```

To run this CWL document run the script below to:

* provide your CDSE username and password to generate and access token
* Use `cwltool` to run stage-and-cog.cwl CWL description  

```console title="terminal"
--8<--
scripts/exec-stage-and-cog.sh
--8<--
```

### Expected outcome

The folder `/workspace/inference-eoap/runs` contains: 

```
(base) jovyan@jupyter-fbrito--training:~/quickwin$ tree runs
runs
TODO
```