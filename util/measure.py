import torch
import time
from thop import profile


# ======================
# Params
# ======================
def count_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


# ======================
# FLOPs
# ======================
def count_flops(model, x):
    model = model.eval()

    flops, params = profile(model, inputs=(x,), verbose=False)

    return flops


# ======================
# Speed test
# ======================
def measure_speed(model, x, warmup=20, repeat=100):

    model = model.eval()

    with torch.no_grad():
        for _ in range(warmup):
            _ = model(x)

    torch.cuda.synchronize()
    start = time.time()

    with torch.no_grad():
        for _ in range(repeat):
            _ = model(x)

    torch.cuda.synchronize()
    end = time.time()

    latency = (end - start) / repeat * 1000
    fps = 1000 / latency

    return latency, fps