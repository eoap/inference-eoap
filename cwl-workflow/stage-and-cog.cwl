cwlVersion: v1.2
$namespaces:
  s: https://schema.org/
s:softwareVersion: 2.0.0
$graph:
- class: Workflow
  id: main
  label: Stage-in and cog-ify a Sentinel-2 L1C acquisition
  doc: Stage-in and cog-ify a Sentinel-2 L1C acquisition
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
      type: '#URI'
    access_token:
      doc: CDSE bearer token
      label: CDSE bearer token
      type: string
  outputs:
  - id: stac_catalog
    outputSource:
    - node_sen2cog/stac_catalog
    type: Directory
    label: stac_catalog
    doc: stac catalog.
  steps:
    node_stage_in:
      run: '#stage-in'
      in:
        item: item
        access_token: access_token
      out:
      - staged
    node_sen2cog:
      run: '#sen2cog'
      in:
        staged:
          source: node_stage_in/staged
      out:
      - stac_catalog
- class: CommandLineTool
  id: stage-in
  requirements:
    NetworkAccess:
      networkAccess: true
    InlineJavascriptRequirement: {}
    EnvVarRequirement:
      envDef:
        PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
        PYTHONPATH: /app
        CDSE_ACCESS_TOKEN: $(inputs.access_token)
    ResourceRequirement:
      coresMax: 1
      ramMin: 1024
      ramMax: 1024
    SchemaDefRequirement:
      types:
      - name: '#URI'
        type: record
        fields:
        - name: value
          type: string
  hints:
    DockerRequirement:
      dockerPull: localhost/stage-in:latest
  baseCommand:
  - python
  - -m
  - app
  arguments: []
  inputs:
    item:
      type: '#URI'
      inputBinding:
        prefix: --input-item
        valueFrom: $(self.value)
      label: item
      doc: item.
    access_token:
      type: string
      label: access_token
      doc: access token.
  outputs:
    staged:
      outputBinding:
        glob: .
      type: Directory
      label: staged
      doc: staged.
  label: stage-in
  doc: 'inference-eoap: stage-in.'
- class: CommandLineTool
  id: sen2cog
  requirements:
    InlineJavascriptRequirement: {}
    EnvVarRequirement:
      envDef:
        PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
        PYTHONPATH: /app
    ResourceRequirement:
      coresMax: 2
      ramMin: 4096
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
      dockerPull: docker.io/library/sen2cog:latest
  baseCommand:
  - python
  - -m
  - app
  arguments: []
  inputs:
    staged:
      type: Directory
      inputBinding:
        prefix: --input-catalog
      label: staged
      doc: staged.
  outputs:
    stac_catalog:
      outputBinding:
        glob: .
      type: Directory
      label: stac_catalog
      doc: stac catalog.
  label: sen2cog
  doc: 'inference-eoap: sen2cog.'
s:codeRepository: https://github.com/eoap/inference-eoap
s:license: https://spdx.org/licenses/CC-BY-SA-4.0.html
s:author:
- class: s:Person
  s:name: Fabrice Brito
  s:email: fabrice.brito@terradue.com
