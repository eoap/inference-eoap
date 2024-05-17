cwlVersion: v1.0
$namespaces:
  s: https://schema.org/
s:softwareVersion: 1.0.0
schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf
$graph:
  - class: Workflow
    id: main
    label: Stage-in and cog-ify a Sentinel-2 L1C acquisition
    doc: Stage-in and cog-ify a Sentinel-2 L1C acquisition
    requirements: {}
    inputs:
      item:
        doc: Reference to a STAC item
        label: STAC item reference
        type: string
      access_token:
        doc: CDSE bearer token
        label: CDSE bearer token
        type: string
    outputs:
      - id: stac_catalog
        outputSource:
          - node_sen2cog/stac_catalog
        type: Directory
    steps:
      node_stage_in:
        run: "#stage-in"
        in:
          item: item
          access_token: access_token
        out:
          - staged
      node_sen2cog:
        run: "#sen2cog"
        in:
          staged:
            source: node_stage_in/staged
        out:
          - stac_catalog
      
  - class: CommandLineTool
    id: stage-in
    requirements:
      InlineJavascriptRequirement: {}
      EnvVarRequirement:
        envDef:
          PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          PYTHONPATH: /app
          CDSE_ACCES_TOKEN: $(inputs.access_token)
      ResourceRequirement:
        coresMax: 1
        ramMax: 1024
    hints:
      DockerRequirement:
        dockerPull: localhost/stage-in:latest
    baseCommand: ["python", "-m", "app"]
    arguments: []
    inputs:
      item:
        type: string
        inputBinding:
          prefix: --input-item
      access_token:
        type: string
    outputs:
      staged:
        outputBinding:
          glob: .
        type: Directory
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
        ramMax: 4096
    hints:
      DockerRequirement:
        dockerPull: docker.io/library/sen2cog:latest
    baseCommand: ["python", "-m", "app"]
    arguments: []
    inputs:
      staged:
        type: Directory
        inputBinding:
          prefix: --input-catalog
    outputs:
      stac_catalog:
        outputBinding:
          glob: .
        type: Directory
  