FROM docker.io/python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends libexpat1 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pystac==1.15.2 click loguru requests numpy rasterio onnx onnxruntime rio-stac && \
    python -c "import rasterio"

ADD app.py /app/app.py
ADD model/sentinel2_classification_trained_model_e50_9190.onnx /app/model/sentinel2_classification_trained_model_e50_9190.onnx

ENTRYPOINT []