import os
from pathlib import Path
from shutil import move

import click
import numpy as np
import onnx
import onnxruntime as ort
import pystac
import rasterio
from affine import Affine
from loguru import logger
from numpy.typing import NDArray
from rasterio.crs import CRS
from rasterio.enums import Resampling
from rio_stac.stac import create_stac_item

from eoap_inference.stac import asset_href, read_item


def sliding(
    shape: tuple[int, int], window_size: int, step_size: int | None = None, fixed: bool = True
) -> list[tuple[int, int, int, int]]:

    h, w = shape
    if step_size:
        h_step = step_size
        w_step = step_size
    else:
        h_step = window_size
        w_step = window_size

    h_wind = window_size
    w_wind = window_size
    windows = []
    for y in range(0, h, h_step):
        for x in range(0, w, w_step):
            h_min = min(h_wind, h - y)
            w_min = min(w_wind, w - x)
            if fixed and (h_min < h_wind or w_min < w_wind):
                continue
            window = (x, y, w_min, h_min)
            windows.append(window)

    return windows


def infer(model_path: str, s2_arr: NDArray[np.float32]) -> NDArray[np.uint8]:
    onnx_model = onnx.load(model_path)

    # Check the model
    onnx.checker.check_model(onnx_model)
    logger.info(f"The model {model_path} is structured correctly.")
    sess = ort.InferenceSession(model_path)
    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name

    logger.info("Divide all image into windows for inference step")

    target_shape = (s2_arr.shape[0], s2_arr.shape[1])
    logger.debug(f"Target shape: {target_shape}")

    windows = sliding(target_shape, 64, fixed=False)

    windows_ = iter(windows)
    windows_class = iter(windows)

    batch_size = 10
    total_chips = len(windows)
    num_steps = (total_chips + batch_size - 1) // batch_size

    # Initialize the classification result array
    img_classes = np.zeros((s2_arr.shape[0], s2_arr.shape[1]), dtype=np.uint8)

    logger.info("Start the inference step")
    for b in range(num_steps):
        logger.info(f"Processing batch {b + 1}/{num_steps}")
        current_batch_size = min(batch_size, total_chips - b * batch_size)
        chips = np.zeros((current_batch_size, 64, 64, 13), dtype=np.float32)
        for k in range(current_batch_size):
            x, y, width, height = next(windows_)
            chips[k, :height, :width] = s2_arr[
                y : y + height, x : x + width, :
            ]  # Adapt based on how your data is structured

        # Run prediction with ONNX
        preds = sess.run([output_name], {input_name: chips.astype(np.float32)})[0]
        classes = np.argmax(preds, axis=-1)

        # Classify the image parts
        for i in range(current_batch_size):
            x, y, width, height = next(windows_class)
            img_classes[y : y + height, x : x + width] = (
                classes[i] if classes.ndim == 1 else classes[i, :height, :width]
            )

    return img_classes


def read_image(src_path: str) -> NDArray[np.float32]:
    with rasterio.open(src_path) as src:
        data = np.asarray(src.read(), dtype=np.float32)

    return data


def stack(item: pystac.Item) -> NDArray[np.float32]:

    bands = [key for key, asset in item.get_assets().items() if "data" in (asset.roles or [])]

    # Prepare array to hold all bands
    all_bands = []

    # Process each band
    for band_key in bands:
        asset = item.assets.get(band_key)
        if asset is not None:
            logger.info(band_key, asset.title)
            # Resize and append to list
            band_data = read_image(asset_href(asset))
            all_bands.append(band_data)
        else:
            logger.info(f"Band {band_key} not found in assets.")

    # Stack all bands into a single numpy array
    all_bands_array = np.stack(all_bands)
    all_bands_array_t = np.transpose(all_bands_array, (2, 3, 1, 0))

    del all_bands_array
    # Squeeze out the singleton dimension (the second last one in this case)
    stacked_array = np.squeeze(all_bands_array_t, axis=2)
    del all_bands_array_t

    return np.asarray(stacked_array, dtype=np.float32)


def get_geocoding(asset_href: str) -> tuple[CRS | None, Affine]:

    with rasterio.open(asset_href) as dataset:
        crs = dataset.crs
        transform = dataset.transform

    return crs, transform


def save_prediction(
    data: NDArray[np.uint8], output_href: str, crs: CRS | None, transform: Affine
) -> None:

    with rasterio.open(
        output_href,
        "w",
        driver="GTiff",
        height=data.shape[0],
        width=data.shape[1],
        count=1,
        dtype=data.dtype,
        crs=crs,
        transform=transform,
        tiled=True,
        blockxsize=256,
        blockysize=256,
        compress="deflate",
        interleave="band",
    ) as dst:
        dst.write(data, 1)
        dst.build_overviews([2, 4, 8, 16], Resampling.nearest)
        dst.update_tags(ns="rio_overview", resampling="nearest")


def to_stac(geotiff_path: str, item: pystac.Item) -> pystac.Item:

    result_item = create_stac_item(
        id=f"{item.id}-classification",
        source=geotiff_path,
        asset_name="classification",
        asset_roles=["data"],
        with_proj=True,
        with_raster=True,
        properties={},
    )

    if not isinstance(result_item, pystac.Item):
        raise TypeError("Raster STAC writer did not return a PySTAC Item")
    return result_item


@click.command(
    short_help="Inference - tile-based classification with ONNX model",
    help="Inference on a STAC Item asset with a trained model",
)
@click.option(
    "--input-item",
    "item_url",
    help="STAC Item URL or staged STAC catalog",
    required=True,
)
def predict(item_url: str) -> None:

    item = read_item(item_url)

    logger.info(f"Read {item.get_self_href()} and stack bands for {item.id}")

    s2_arr = stack(item)
    logger.debug(f"Stacked array shape: {s2_arr.shape}")

    prediction = infer(
        model_path=str(
            Path(__file__).with_name("model")
            / "sentinel2_classification_trained_model_e50_9190.onnx"
        ),
        s2_arr=s2_arr,
    )

    logger.debug(f"Prediction shape: {prediction.shape}")

    crs, transform = get_geocoding(asset_href(item.assets["red"]))

    save_prediction(prediction, "classification.tif", crs, transform)

    out_item = to_stac("classification.tif", item)

    logger.info("Creating a STAC Catalog for the classification result")
    cat = pystac.Catalog(
        id="catalog", description="classification result", title="classification result"
    )
    cat.add_items([out_item])

    cat.normalize_and_save(root_href="./", catalog_type=pystac.CatalogType.SELF_CONTAINED)
    move("classification.tif", os.path.join(out_item.id, "classification.tif"))
    logger.info("Done!")


if __name__ == "__main__":
    predict()
