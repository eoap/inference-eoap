### Goal

Wrap the CommandLineTool with a CWL Workflow

### Lab

This step has a dedicated lab available at `/workspace/inference-eoap/practice-labs/Workflow.ipynb`

### How to wrap a CWL CommandLineTool with a CWL Workflow

The Cloud native Workflow orchestrates the wrapped Python application command line tool as a CWL `CommandLineTool` step with input parameters:

* a staged and converted to COG Sentinel-2 Level-1C acquisition 

``` mermaid
graph TB
A[STAC Catalog]
A --> B(("Inference"));
B --> C[STAC Catalog]
```

The CWL Workflow is shown below and the lines highlighted chain the inference step:

```yaml linenums="1" title="tile-based-classification.cwl"
--8<--
cwl-workflow/tile-based-classification.cwl
--8<--
```

To run this CWL document, one does:

```console title="terminal"
--8<--
scripts/cwl-workflow.sh
--8<--
```

### Expected outcome

The folder `/workspace/inference-eoap/runs` contains: 

```
(base) jovyan@jupyter-fbrito--training:~/inference-eoap$ tree runs
runs
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

2 directories, 16 files
```