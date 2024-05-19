## Inference

### Step purpose 

Purpose: apply the inference function loaded from an ONNX model to a Sentinel-2 Level-1C staged and converted to COG. The output is a tile based classification encoded as a STAC Catalog with a STAC Item.

### Code

The `predict.py` script is a command-line tool designed for performing inference on Sentinel-2 Level-1C product assets using a pre-trained ONNX model. The output is a classified image saved as a GeoTIFF file and a corresponding STAC Item with the classification results. 

This process involves stacking bands, dividing the image into tiles, running inference, and saving the results. 

The script uses Python libraries such as `pystac`, `rasterio`, `onnx`, `onnxruntime`, `numpy`, `click`, and `loguru`.

### Functionalities and Flow

Importing Required Libraries:

* `os`: For interacting with the operating system (e.g., file paths).
* `shutil.move`: For moving files.
* `numpy`: For numerical operations.
* `onnx`: For working with ONNX models.
* `onnxruntime`: For running inference using ONNX models.
* `rasterio`: For reading and writing geospatial raster data.
* `pystac`: For working with STAC items and catalogs.
* `click`: For creating command-line interfaces.
* `loguru`: For logging.

Helper Functions:

* `sliding(shape, window_size, step_size=None, fixed=True)`:

Generates a list of windows (tiles) for sliding over the input image.
Each window is defined by its coordinates (x, y, width, height).
infer(model_path: str, s2_arr: np.ndarray) -> np.ndarray:
Loads the ONNX model and checks its structure.
Divides the input image into windows and runs inference on each window.
Assembles the prediction results into a classified image.

* `read_image(src_path: str) -> np.ndarray`:

Reads the raster data from the specified file path and returns it as a numpy array.

* `stack(item: pystac.Item) -> np.ndarray`:

Stacks the bands of the input STAC Item into a single numpy array.
Each band is resized and appended to the list, which is then stacked and transposed.

* `get_geocoding(asset_href: str) -> (rasterio.crs.CRS, Affine)`:

Retrieves the coordinate reference system (CRS) and transformation matrix from the specified asset.
save_prediction(data: np.ndarray, output_href: str, crs: rasterio.crs.CRS, transform: Affine):
Saves the classified image data to a GeoTIFF file with specified CRS and transform.
Builds overviews for the output GeoTIFF file.

* `to_stac(geotiff_path: str, item: pystac.Item) -> pystac.Item`:

Creates a new STAC Item for the classified GeoTIFF file.
Uses rio_stac to generate the STAC Item with the necessary metadata.

Main Function: `predict`

* Reading the STAC Item:

Reads the STAC Item from the provided URL or path.

* Stacking Bands:

Stacks the bands of the STAC Item into a single numpy array.

* Running Inference:

Runs inference using the pre-trained ONNX model on the stacked array.
Divides the image into windows and processes each batch.

* Saving the Prediction:

Saves the prediction result as a GeoTIFF file.
Retrieves the geocoding information (CRS and transform) from one of the bands.

* Creating a New STAC Item:

Creates a new STAC Item for the classified image.
Adds the new STAC Item to a catalog and saves it as a self-contained STAC Catalog.

* Moving Output File:

Moves the classified GeoTIFF file to the output directory.


#### Script Execution 

The script is executable as a command-line tool as its usage is:

```
Usage: python -m app.app [OPTIONS]

  Inference on a STAC Item asset with a trained model

Options:
  --input-item TEXT  STAC Item URL or staged STAC catalog  [required]
  --help             Show this message and exit.
```

#### Listing

The Python code is provided here:

```python linenums="1" title="tile-based-classification/command-line-tools/inference/app.py"
--8<--
tile-based-classification/command-line-tools/inference/app.py
--8<--
```