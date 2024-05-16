import os
import rasterio
import pystac
import click
from shutil import move
from loguru import logger
from rasterio.enums import Resampling
from pystac.extensions.eo import EOExtension


def resize_and_convert_to_cog(src_path, output_path, target_resolution=(10, 10)):
    with rasterio.open(src_path) as src:
        # Calculate the new shape based on the target resolution
        scale_x = src.width * (src.res[0] / target_resolution[0])
        scale_y = src.height * (src.res[1] / target_resolution[1])
        logger.info(f"Resizing image to {scale_x}x{scale_y}")
        # Read and resample data
        data = src.read(
            out_shape=(src.count, int(scale_y), int(scale_x)),
            resampling=Resampling.bilinear,
        )

        # Update the metadata for the transformed dataset
        transform = src.transform * src.transform.scale(
            (src.width / data.shape[-1]), (src.height / data.shape[-2])
        )
        profile = src.profile
        profile.update(
            {
                "driver": "COG",
                "dtype": data.dtype,
                "height": data.shape[1],
                "width": data.shape[2],
                "transform": transform,
                "compress": "LZW",
                "interleave": "pixel",
            }
        )

        # Write data directly to a COG file
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(data)

@click.command(
    short_help="Convert a Sentinel-2 to COG",
    help="Convert a Sentinel-2 Level-1C product to COG format. The output is a STAC Item with COG assets.",
)
@click.option(
    "--input-catalog",
    "catalog_url",
    help="STAC Catalog with an Sentinel-2 Level-1C item",
    required=True,
)
def to_cog(catalog_url):

    if os.path.isdir(catalog_url):
        catalog = pystac.read_file(os.path.join(catalog_url, "catalog.json"))
        item = next(catalog.get_items())
    else:
        item = pystac.read_file(catalog_url)

    os.makedirs(item.id, exist_ok=True)
    item_out = pystac.Item(
        id=f"{item.id}",
        geometry=item.geometry,
        bbox=item.bbox,
        datetime=item.datetime,
        properties=item.properties,
    )
    eo = EOExtension.ext(item_out, add_if_missing=True)

    logger.info(f"Read {item.get_self_href()} and stack bands for {item.id}")

    # loop through the assets and convert them to COG
    for key, asset in item.get_assets().items():
        logger.info(f"Converting asset {key} to COG")
        if "data" not in asset.roles:
            continue

        output_cog_file_path = f"{key}.tif"
        resize_and_convert_to_cog(
            asset.get_absolute_href(), output_cog_file_path, target_resolution=(10, 10)
        )
        logger.info(f"COG file created: {output_cog_file_path}")

        # create a new asset for the COG file
        cog_asset = pystac.Asset(
            href=output_cog_file_path, media_type=pystac.MediaType.COG, roles=["data"]
        )
        src_eo_asset = EOExtension.ext(asset)

        item_out.add_asset(key, asset=cog_asset)
        # add eo extension to the asset

        logger.info(f"Adding EO extension to asset {key}")
        eo_on_asset = EOExtension.ext(item_out.assets[key])
        eo_on_asset.apply(src_eo_asset.bands)

        move(output_cog_file_path, os.path.join(item.id, output_cog_file_path))
        
    cat = pystac.Catalog(
        id="catalog", description="sen2cog result", title="sen2cog result"
    )
    cat.add_items([item_out])

    cat.normalize_and_save(
        root_href="./", catalog_type=pystac.CatalogType.SELF_CONTAINED
    )

    print(item_out.to_dict())

if __name__ == "__main__":
    to_cog()
