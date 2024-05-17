# Tile based classification

The tile based classification application takes a trained model in the ONNX format and does the inference on Sentinel-2 Level-1C data.

The model was trained using a Sequential Convolutional Neural Network (CNN) with Keras based on the benchmark dataset EuroSAT. 

## Training Data

The model is trained on the EuroSAT benchmark dataset which is based on Sentinel-2 satellite images and consists of a total of 27,000 labeled and geo-referenced images. 

The dataset provides information on the following ten land cover / land use classes:

* Annual Crop
* Forest
* Herbaceous Vegetation
* Highway
* Industrial
* Pasture
* Permanent Crop
* Residential
* River
* Sea Lake

The benchmark dataset can be used to detect land cover/land use changes. 

## Inference

The inference is the process where the learned capabilities of a pre-trained model are put into practice and applied to a Sentinel-2 Level-1C acquisition.

This application foresees using Sentinel-2 Level-1C data converted to COG and structured as a STAC Catalog and Item.

There is a pre-processing step to stage and convert to STAC/COG a Sentinel-2 Level-1C acquisition then used for the inference process.

The inference step loads the pre-trained model and executes the inference process, which 'infers' land cover classes.

