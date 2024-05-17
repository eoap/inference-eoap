import os
import zipfile
import click
import pystac 
import requests
from stactools.sentinel2.stac import create_item
from loguru import logger

def get_asset_href(item, asset_key):
    """Returns the asset of a STAC Item defined with its asset key"""
    for key, asset in item.get_assets().items():
        if key in [asset_key]:    
            return asset.href.replace("catalogue", "zipper")

def download_and_extract_file(item: pystac.Item, access_token: str):
    
    headers = {"Authorization": f"Bearer {access_token}"}

    session = requests.Session()
    session.headers.update(headers)
    response = session.get(get_asset_href(item, "PRODUCT"), headers=headers, stream=True)

    with open("product.zip", "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
    with zipfile.ZipFile("product.zip", "r") as zip_ref:
        zip_ref.extractall(".")
    
    return os.path.join(os.getcwd(), item.id)

@click.command(
    short_help="Stage-in",
    help="Stage a Sentinel-2 Level-1C product",
)
@click.option(
    "--input-item",
    "item_url",
    help="Sentinel-2 Level-1C CDSE STAC Item URL",
    required=True,
)
def stage(item_url):
    
    logger.info(f"Staging {item_url}")
    item = pystac.read_file(item_url)
    
    access_token = os.environ.get("CDSE_ACCES_TOKEN")
    
    logger.info("Downloading and extracting file")
    staged_s2 = download_and_extract_file(item, access_token)
    
    logger.info("Creating STAC Item")
    s2_item = create_item(
        granule_href=staged_s2,
    )

    item_path = os.path.join(".", f"{s2_item.id}.json")
    s2_item.set_self_href(item_path)

    s2_item.save_object(include_self_link=False, dest_href=item_path)

    logger.info("Creating STAC Catalog")
    cat = pystac.Catalog(
        id="catalog",
        description=f"catalog with staged {s2_item.id}",
        title=f"catalog with staged {s2_item.id}",
    )
    s2_item.make_asset_hrefs_relative()
    cat.add_item(s2_item)

    cat.normalize_hrefs("./")
    cat.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

    logger.info("Done!")
    
if __name__ == "__main__":
    stage()