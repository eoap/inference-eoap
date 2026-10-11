"""The real ONNX artifact must survive both editable and wheel installations."""

from pathlib import Path

import onnx

from eoap_inference import inference


def test_packaged_scientific_model_is_valid():
    path = (
        Path(inference.__file__).with_name("model")
        / "sentinel2_classification_trained_model_e50_9190.onnx"
    )
    onnx.checker.check_model(onnx.load(str(path)))
