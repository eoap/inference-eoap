FROM docker.io/python:3.10-slim

RUN pip install --no-cache-dir pystac==1.9.0 click loguru requests numpy rasterio onnx onnxruntime rio-stac && \
    python -c "import rasterio"

ADD app.py /app/app.py
ADD model/sentinel2_classification_trained_model_e50_9190.onnx /app/model/sentinel2_classification_trained_model_e50_9190.onnx

ENTRYPOINT []