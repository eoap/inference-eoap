FROM docker.io/library/python:3.12.11-bookworm@sha256:bea386df48d7ee07eed0a1f3e6f9d5c0292c228b8d8ed2ea738b7a57b29c4470
COPY requirements-runtime.txt /tmp/requirements-runtime.txt
RUN pip install --no-cache-dir --require-hashes -r /tmp/requirements-runtime.txt
COPY tile-based-classification/command-line-tools/sen2cog/app.py /app/app.py
ENTRYPOINT []
