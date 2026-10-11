"""Compatibility entry point for the published CWL command."""
from eoap_inference.inference import predict as predict

if __name__ == "__main__":
    predict()
