"""Create a local 13-band STAC fixture; inference still uses the real ONNX model."""
from datetime import datetime, timezone
from pathlib import Path
import json
import numpy as np
import pystac
import rasterio
from rasterio.transform import from_origin

root = Path(__file__).resolve().parents[1] / "runs"
source = root / "fixture"
source.mkdir(parents=True, exist_ok=True)
item = pystac.Item(id="local-sentinel-fixture", geometry={"type": "Polygon", "coordinates": [[[12, 42], [12.03, 42], [12.03, 42.03], [12, 42.03], [12, 42]]]}, bbox=[12, 42, 12.03, 42.03], datetime=datetime(2024, 1, 25, tzinfo=timezone.utc), properties={})
names = ["coastal", "blue", "green", "red", "rededge1", "rededge2", "rededge3", "nir", "nir08", "water_vapour", "cirrus", "swir16", "swir22"]
# Sixteen 64x64 chips exercise the final partial batch of six chips.
y, x = np.indices((256, 256))
for index, name in enumerate(names):
    path = source / (name + ".tif")
    values = (1000 + index * 200 + (x + y) % 500).astype("uint16")
    with rasterio.open(path, "w", driver="GTiff", height=256, width=256, count=1, dtype="uint16", crs="EPSG:4326", transform=from_origin(12, 42.03, 0.0001, 0.0001), tiled=True, blockxsize=64, blockysize=64) as dataset:
        dataset.write(values, 1)
    item.add_asset(name, pystac.Asset(href=str(path), media_type=pystac.MediaType.GEOTIFF, roles=["data"]))
catalog = pystac.Catalog(id="local-staging-fixture", description="Deterministic local staging fixture; real inference model")
catalog.add_item(item)
catalog.normalize_hrefs(str(source))
catalog.make_all_asset_hrefs_relative()
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
(root / "results.json").write_text(json.dumps({"stac_catalog": {"class": "Directory", "path": str(source), "location": source.as_uri()}}, indent=2))
print(source / "catalog.json")
