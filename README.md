# Inference with the EO Application Package

This repository contains an EO Application Package that wraps an inference function for performing tile-based classification on Sentinel-2 Level-1C data.

The classification is based on a model trained using a Sequential Convolutional Neural Network (CNN) with Keras, utilizing the benchmark dataset [EuroSAT](https://github.com/phelber/EuroSAT). The trained model, saved in ONNX format, is packaged in the Application Package and used to perform inference on new Sentinel-2 data. 

The webpage of the documentation is https://eoap.github.io/inference-eoap/. 

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)