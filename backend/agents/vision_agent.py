import io

import numpy as np
from PIL import Image


def analyze(data: bytes) -> dict:
    """Pixel statistics always; ResNet18 embedding when torch/torchvision are installed."""
    im = Image.open(io.BytesIO(data)).convert("RGB")
    a = np.asarray(im.resize((256, 256)), dtype=float)
    g = a.mean(axis=2)
    out = {"size": im.size, "brightness": round(float(g.mean()), 1),
           "edge_density": round(float((np.abs(np.diff(g, axis=0)) > 40).mean()), 3)}
    try:
        import torch
        import torchvision.models as m
        net = m.resnet18(weights=m.ResNet18_Weights.DEFAULT).eval()
        t = torch.tensor(a / 255.0, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0)
        with torch.no_grad():
            out["cnn_embedding_norm"] = round(float(net(t).norm()), 2)
    except Exception:
        out["cnn"] = "torch not installed: pixel features only"
    return out
