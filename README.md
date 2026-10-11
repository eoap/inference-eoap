# Inference with the EO Application Package

This repository contains an EO Application Package that wraps an inference function for performing tile-based classification on Sentinel-2 Level-1C data.

The classification is based on a model trained using a Sequential Convolutional Neural Network (CNN) with Keras, utilizing the benchmark dataset [EuroSAT](https://github.com/phelber/EuroSAT). The trained model, saved in ONNX format, is packaged in the Application Package and used to perform inference on new Sentinel-2 data. 

The webpage of the documentation is https://eoap.github.io/inference-eoap/. 

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
## Typed CWL and PDE validation

Application packages use CWL v1.2, embedded URI records, described ports and
Schema.org repository/version/license/author metadata. Generate and validate
standalone documentation with `python scripts/cwl-docs.py --validate`.
The PDE deployment and executable lab tasks are in the sibling
`dev-platform-eoap/inference-eoap` folder. Feature-branch changes must be published
or copied into its retained workspace before deployment.

For offline staging acceptance, `python scripts/create-fixture.py` creates a
portable 13-band STAC catalog with sixteen chips. Notebook execution with
`EOAP_INFERENCE_LOCAL_FIXTURE=1` uses that fixture and the real ONNX model.
Authenticated CDSE downloading remains an explicit separate lab path using
credentials from environment variables. The inference loop now processes the
final partial batch, verified by `python -m pytest tests`. All six notebooks
and standalone contract checks passed on AMD64 Kubernetes on 11 October 2026.

## Preparing 2.0.0

The intended release adds authenticated Copernicus S3 staging and fixes partial
batch and edge-chip classification. Processing containers share hashed Python
3.12 dependencies and a digest-pinned base image. Build from the repository
root, for example:

```sh
docker build -f tile-based-classification/command-line-tools/stage-in/Dockerfile -t localhost/stage-in:latest .
```

The staging tool accepts `CDSE_S3_ACCESS_KEY` and `CDSE_S3_SECRET_KEY` (or standard
AWS credential variables), with endpoint `https://eodata.dataspace.copernicus.eu`.
It downloads the complete SAFE product referenced by the current CDSE STAC item,
checks object sizes and derives the catalog from the real product metadata.
The token path instead uses `CDSE_ACCESS_TOKEN`; `bin/get-bearer-token` accepts
`CDSE_USERNAME` and `CDSE_PASSWORD` from the environment.

Platform task `labs:authenticated` reads the platform `.env`, sends credentials
through Kubernetes exec stdin, keeps SeaweedFS credentials separate, and redacts
credentials from execution logs and saved notebooks. It runs all six notebooks
with real Sentinel-2 input. The synthetic fixture remains a development check;
it cannot establish scientific release acceptance.

CI checks regressions, standalone contracts and all three container builds.
Feature pushes and explicit workflow dispatch with `publish_candidate=true` publish
`2.0.0-rc.<run-number>` images and a checksummed artifact containing all three
CWL entrypoints pinned to the pushed image digests. It does not publish a stable
release. Record authenticated notebook and scientific output acceptance for the
intended commit, then validate the published candidate artifacts before promotion.

`download-app-inference.sh` defaults to the current source package, allowing
pre-release tests without downloading an older stable workflow. Set
`EOAP_ARTIFACT_MODE=release` and `EOAP_RELEASE_VERSION=<candidate-or-stable-tag>`
when testing matching published GitHub release assets. No packing command is used.
