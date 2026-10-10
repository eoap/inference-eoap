"""The inference loop must classify all chips, including a partial batch."""
import importlib.util
from pathlib import Path
from unittest.mock import patch
import numpy as np

path = Path(__file__).resolve().parents[1] / "tile-based-classification/command-line-tools/inference/app.py"
spec = importlib.util.spec_from_file_location("inference", path)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

class Session:
    def get_inputs(self):
        return [type("Input", (), {"name": "input"})()]
    def get_outputs(self):
        return [type("Output", (), {"name": "output"})()]
    def run(self, names, inputs):
        chips = inputs["input"]
        prediction = np.zeros((*chips.shape[:3], 2), dtype=np.float32)
        prediction[..., 1] = 1
        return [prediction]

def test_partial_batch_is_not_dropped():
    with patch.object(app.onnx, "load"), patch.object(app.onnx.checker, "check_model"), patch.object(app.ort, "InferenceSession", return_value=Session()):
        classified = app.infer("unused", np.ones((256, 256, 13), dtype=np.float32))
    assert classified.shape == (256, 256)
    assert np.all(classified == 1)
