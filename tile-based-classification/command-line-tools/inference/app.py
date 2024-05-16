import os
from shutil import move
import numpy as np
import onnx
import onnxruntime as ort
import rasterio
import pystac
import click
from loguru import logger
from rasterio.enums import Resampling
from rio_stac.stac import create_stac_item



def sliding(shape, window_size, step_size=None, fixed=True):

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
            if fixed:
                if h_min < h_wind or w_min < w_wind:
                    continue
            window = (x, y, w_min, h_min)
            windows.append(window)

    return windows


def infer(model_path, s2_arr):
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

    windows = sliding(target_shape, 64, fixed=True)

    windows_ = iter(windows)
    windows_class = iter(windows)

    batch_size = 10
    total_chips = len(windows)
    num_steps = int(total_chips / batch_size)

    # Initialize the classification result array
    img_classes = np.zeros((s2_arr.shape[0], s2_arr.shape[1]), dtype=np.uint8)

    predictions = []

    logger.info("Start the inference step")
    for b in range(num_steps):
        logger.info(f"Processing batch {b+1}/{num_steps}")
        chips = np.empty((batch_size, 64, 64, 13))
        for k in range(batch_size):
            ymin, xmin, xmax, ymax = next(windows_)
            chips[k] = s2_arr[
                xmin : xmin + xmax, ymin : ymin + ymax, :
            ]  # Adapt based on how your data is structured

        # Run prediction with ONNX
        preds = sess.run([output_name], {input_name: chips.astype(np.float32)})[0]
        predictions.append(np.argmax(preds, axis=-1))

        # Classify the image parts
        for i in range(batch_size):
            ymin_cl, xmin_cl, xmax_cl, ymax_cl = next(windows_class)
            img_classes[xmin_cl : xmin_cl + xmax_cl, ymin_cl : ymin_cl + ymax_cl] = (
                predictions[b][i]
            )

    return img_classes


def read_image(src_path):
    with rasterio.open(src_path) as src:
        data = src.read()

    return data


def stack(item):

    bands = [key for key, asset in item.get_assets().items() if "data" in asset.roles]

    # Prepare array to hold all bands
    all_bands = []

    # Process each band
    for band_key in bands:
        asset = item.assets.get(band_key)
        if asset is not None:
            logger.info(band_key, asset.title)
            # Resize and append to list
            band_data = read_image(asset.get_absolute_href())
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

    return stacked_array


def get_geocoding(asset_href):

    with rasterio.open(asset_href) as dataset:
        crs = dataset.crs
        transform = dataset.transform

    return crs, transform


def save_prediction(data, output_href, crs, transform):

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


def to_stac(geotiff_path, item):

    result_item = create_stac_item(
        id=f"{item.id}-classification",
        source=geotiff_path,
        asset_name="classification",
        asset_roles=["data"],
        with_proj=True,
        with_raster=True,
        properties={},
    )

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
def predict(item_url):

    if os.path.isdir(item_url):
        catalog = pystac.read_file(os.path.join(item_url, "catalog.json"))
        item = next(catalog.get_items())
    else:
        item = pystac.read_file(item_url)

    logger.info(f"Read {item.get_self_href()} and stack bands for {item.id}")

    s2_arr = stack(item)
    logger.debug(f"Stacked array shape: {s2_arr.shape}")

    prediction = infer(
        model_path=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "model",
            "sentinel2_classification_trained_model_e50_9190.onnx",
        ),
        s2_arr=s2_arr,
    )

    logger.debug(f"Prediction shape: {prediction.shape}")

    crs, transform = get_geocoding(item.assets.get("red").get_absolute_href())

    save_prediction(prediction, "classification.tif", crs, transform)

    out_item = to_stac("classification.tif", item)

    logger.info(f"Creating a STAC Catalog for the classification result")
    cat = pystac.Catalog(
        id="catalog", description="classification result", title="classification result"
    )
    cat.add_items([out_item])

    cat.normalize_and_save(
        root_href="./", catalog_type=pystac.CatalogType.SELF_CONTAINED
    )
    move("classification.tif", os.path.join(out_item.id, "classification.tif"))
    logger.info("Done!")


if __name__ == "__main__":
    predict()
