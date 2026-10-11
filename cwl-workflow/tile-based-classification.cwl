cwlVersion: v1.2
$namespaces:
  s: https://schema.org/
s:softwareVersion: 2.0.0
$graph:
- class: Workflow
  id: main
  label: Sentinel-2 Level-1C Tile Based Classification
  doc: Sentinel-2 Level-1C Tile Based Classification based on EUROSAT dataset
  requirements:
    InlineJavascriptRequirement: {}
    SchemaDefRequirement:
      types:
      - name: '#URI'
        type: record
        fields:
        - name: value
          type: string
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
    label: stac_catalog
    doc: stac catalog.
  steps:
    node_inference:
      run: '#inference'
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
    SchemaDefRequirement:
      types:
      - name: '#URI'
        type: record
        fields:
        - name: value
          type: string
  hints:
    DockerRequirement:
      dockerPull: localhost/inference:latest
  baseCommand:
  - python
  - -m
  - app
  arguments: []
  inputs:
    input-item:
      type: Directory
      inputBinding:
        prefix: --input-item
      label: input-item
      doc: input item.
  outputs:
    stac_catalog:
      outputBinding:
        glob: .
      type: Directory
      label: stac_catalog
      doc: stac catalog.
  label: inference
  doc: 'inference-eoap: inference.'
s:codeRepository: https://github.com/eoap/inference-eoap
s:license: https://spdx.org/licenses/CC-BY-SA-4.0.html
s:author:
- class: s:Person
  s:name: Fabrice Brito
  s:email: fabrice.brito@terradue.com
