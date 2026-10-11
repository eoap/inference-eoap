"""Prepare immutable release CWL without packing or changing source documents."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import yaml

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--version', required=True)
parser.add_argument('--images', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
images = {}
for path in args.images.glob('*.json'):
    images.update(json.loads(path.read_text()))
for name in ('stage-in', 'sen2cog', 'inference'):
    assert re.fullmatch(r'ghcr.io/eoap/inference-eoap/'+name+r':[^@]+@sha256:[0-9a-f]{64}', images[name]), name
args.output.mkdir(parents=True, exist_ok=True)
checksums = []
for source in sorted([*(root/'cwl-workflow').glob('*.cwl'), *(root/'cwl-cli').glob('*.cwl')]):
    document = yaml.safe_load(source.read_text())
    assert document['cwlVersion'] == 'v1.2'
    document['s:softwareVersion'] = args.version
    for process in document.get('$graph', [document]):
        for group in ('requirements', 'hints'):
            docker = process.get(group, {}).get('DockerRequirement')
            if docker:
                name = docker['dockerPull'].split('/')[-1].split(':')[0]
                docker['dockerPull'] = images[name]
    output = args.output/(source.stem+'.'+args.version+'.cwl')
    output.write_text(yaml.safe_dump(document, sort_keys=False))
    checksums.append(hashlib.sha256(output.read_bytes()).hexdigest()+'  '+output.name)
(args.output/'SHA256SUMS').write_text('\n'.join(checksums)+'\n')
(args.output/'images.json').write_text(json.dumps(images,indent=2)+'\n')
