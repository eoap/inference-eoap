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
