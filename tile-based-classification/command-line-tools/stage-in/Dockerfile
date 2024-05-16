FROM docker.io/python:3.10-slim

RUN pip install --no-cache-dir pystac==1.9.0 click loguru requests stactools-sentinel2 && \
    python -c "import rasterio"

ADD app.py /app/app.py

ENTRYPOINT []