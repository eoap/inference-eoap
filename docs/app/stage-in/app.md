# Sentinel-2 Level-1C stage-in



### Step purpose 

Purpose: While there are many options to consume Sentinel-2 Level-2A in a Cloud native processing approach, the Level-1C data must instead be staged from the Copernicus Data Space Ecosystem. The output is a STAC Catalog referencing a local STAC Item with the Sentinel-2 Level-1C files (assets) available in the local filesystem

This step is highlighted below:

``` mermaid
graph TB

```

### Code

The `stage-in.py` script is a command-line tool designed to stage Sentinel-2 Level-1C products. It downloads, extracts, and creates STAC (SpatioTemporal Asset Catalog) items from a provided STAC item URL. This process involves handling asset URLs, downloading and extracting files, and generating a catalog. 

The script leverages Python libraries such as `pystac`, `requests`, `click`, `loguru`, and `stactools.sentinel2.stac`.

#### Functionalities and Flow

Importing Required Libraries:

* `os`: For interacting with the operating system (e.g., file paths).
* `zipfile`: For handling zip file extraction.
* `click`: For creating command-line interfaces.
* `pystac`: For working with STAC items and catalogs.
* `requests`: For making HTTP requests.
* `loguru`: For logging.
* `stactools.sentinel2.stac`: For creating STAC items specific to Sentinel-2 products.

Helper Functions:

* `get_asset_href(item: pystac.Item, asset_key: str) -> str`:

Retrieves the asset URL of a STAC Item given its asset key.
Replaces "catalogue" with "zipper" in the asset's href to get the correct download URL.

* `download_and_extract_file(item: pystac.Item, access_token: str) -> str`:

Downloads and extracts the asset file from a STAC Item using an access token.
Sets up headers for authorization and makes a request to download the file.
Saves the downloaded file as "product.zip" and extracts it.
Returns the path to the extracted files.

Here is an overview of the script's functionality:

Staging Process:

* Logs the staging process.
* Reads the STAC Item from the provided URL using `pystac`.
* Retrieves the access token from the environment variable `CDSE_ACCESS_TOKEN`.
* Downloads and extracts the file using `download_and_extract_file`.

Creating STAC Item:

* Uses create_item from `stactools.sentinel2.stac` to create a STAC Item from the extracted files.
* Sets the self-href for the STAC Item and saves it to a JSON file.

Creating STAC Catalog:

* Creates a STAC Catalog, adds the STAC Item, and normalizes hrefs.
* Saves the catalog as a self-contained STAC Catalog.

The script is executable as a command-line tool as its usage is:

```
Usage: python -m app.app [OPTIONS]

  Stage a Sentinel-2 Level-1C product

Options:
  --input-item TEXT  Sentinel-2 Level-1C CDSE STAC Item URL  [required]
  --help             Show this message and exit.
```

The Python code is provided here:

--8<--
tile-based-classification/command-line-tools/stage-in/app.py
--8<--