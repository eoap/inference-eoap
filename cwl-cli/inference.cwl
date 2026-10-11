cwlVersion: v1.2
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
    ramMin: 8192
    ramMax: 8192
  SchemaDefRequirement:
    types:
    - $import: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml
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
$namespaces:
  s: https://schema.org/
s:softwareVersion: 2.0.0
s:codeRepository: https://github.com/eoap/inference-eoap
s:license: https://spdx.org/licenses/CC-BY-SA-4.0.html
s:author:
- class: s:Person
  s:name: Fabrice Brito
  s:email: fabrice.brito@terradue.com
label: inference
doc: 'inference-eoap: inference.'
