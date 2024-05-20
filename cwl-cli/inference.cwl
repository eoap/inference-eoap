cwlVersion: v1.0

class: CommandLineTool
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
  