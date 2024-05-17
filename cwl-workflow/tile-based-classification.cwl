cwlVersion: v1.0
$namespaces:
  s: https://schema.org/
s:softwareVersion: 1.0.0
schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf
$graph:
  - class: Workflow
    id: main
    label: Sentinel-2 Level-1C Tile Based Classification
    doc: Sentinel-2 Level-1C Tile Based Classification based on EUROSAT dataset
    requirements: {}
    inputs:
      item:
        doc: Reference to a STAC item
        label: STAC item reference
        type: Directory
    outputs:
      - id: stac_catalog
        outputSource:
          - node_inference/stac_catalog
        type: Directory
    steps:
      node_inference:
        run: "#inference"
        in:
          input-item: item
        out:
          - stac_catalog
  - class: CommandLineTool
    id: inference
    requirements:
      InlineJavascriptRequirement: {}
      EnvVarRequirement:
        envDef:
          PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          PYTHONPATH: /app
      ResourceRequirement:
        coresMax: 2
        ramMax: 4096
    hints:
      DockerRequirement:
        dockerPull: localhost/inference:latest
    baseCommand: ["python", "-m", "app"]
    arguments: []
    inputs:
      input-item:
        type: Directory
        inputBinding:
          prefix: --input-item
    outputs:
      stac_catalog:
        outputBinding:
          glob: .
        type: Directory
  