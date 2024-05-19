python3 -m venv env_inference
source env_inference/bin/activate
pip install --no-cache-dir pystac==1.9.0 click loguru requests numpy rasterio onnx onnxruntime rio-stac