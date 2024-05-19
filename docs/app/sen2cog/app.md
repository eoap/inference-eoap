## Stages Sentinel-2 Level-1C conversion to COG

### Step purpose 

Purpose: convert the Sentinel-2 Level-1 jp2 assets to COG and resample the 20m and 60m resolution bands to 10m

### Code

The `to_cog.py` script is a command-line tool designed to convert Sentinel-2 Level-1C product assets to Cloud Optimized GeoTIFF (COG) format. The output is a STAC Item with COG assets.

This process involves reading a STAC Catalog, resizing and converting assets, and creating a new STAC Item with the converted assets. 

The script uses Python libraries such as `pystac`, `rasterio`, `click`, and `loguru`.

#### Functionalities and Flow

Importing Required Libraries:

* `os`: For interacting with the operating system (e.g., file paths).
* `rasterio`: For reading and writing geospatial raster data.
* `pystac`: For working with STAC items and catalogs.
* `click`: For creating command-line interfaces.
* `loguru`: For logging.
* `shutil.move`: For moving files.

Helper Function:

* `resize_and_convert_to_cog(src_path: str, output_path: str, target_resolution=(10, 10))`:

Resizes the image to the target resolution and converts it to COG format.
Opens the source file and calculates the new shape based on the target resolution.
Reads and resamples the data using bilinear resampling.
Updates the metadata for the transformed dataset and writes the data to a COG file with LZW compression.

Command-line Interface:

Defined using `click` with an option for the input STAC Catalog URL.

Options:

* `--input-catalog`: URL or path of the STAC Catalog containing a Sentinel-2 Level-1C item (required).

Here is an overview of the script's functionality:

Reading the STAC Catalog:

* Reads the STAC Catalog from the provided URL or path.
* Retrieves the first item from the catalog.

Setting Up Output Directory:

* Creates a directory named after the item ID if it doesn't exist.

Creating a New STAC Item:

* Creates a new STAC Item with the same properties as the original item.
* Adds the EO extension to the new item.

Converting Assets to COG:

* Iterates through the assets of the original item and converts each asset with the role "data" to COG format.
* Resizes and converts the asset using resize_and_convert_to_cog.
* Creates a new asset for the COG file and adds it to the new item.
* Moves the COG file to the output directory.

Creating a New STAC Catalog:

* Creates a new STAC Catalog and adds the new item to it.
* Normalizes and saves the catalog as a self-contained STAC Catalog.

#### Script Execution 

The script is executable as a command-line tool as its usage is:

```
Usage: python -m app.app [OPTIONS]

  Convert a Sentinel-2 Level-1C product to COG format. The output is a STAC
  Item with COG assets.

Options:
  --input-catalog TEXT  STAC Catalog with an Sentinel-2 Level-1C item
                        [required]
  --help                Show this message and exit.
```

#### Listing

The Python code is provided here:

```python linenums="1" title="tile-based-classification/command-line-tools/sen2cog/app.py"
--8<--
tile-based-classification/command-line-tools/sen2cog/app.py
--8<--
```