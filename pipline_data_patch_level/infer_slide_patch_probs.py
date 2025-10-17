import json
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import openslide
import h5py
import torch
import torch.nn as nn
from torchvision import models, transforms

SLIDE_ID = "CMU-2"
SLIDE_PATH = f"/Users/yhu10/Desktop/VLM/pipline_data_patch_level/data/slides/{SLIDE_ID}.svs"
H5_PATH    = f"/Users/yhu10/Desktop/VLM/pipline_data_patch_level/data/patches/{SLIDE_ID}.h5"
CKPT       = f"/Users/yhu10/Desktop/VLM/pipline_data_patch_level/runs/patch_clf/resnet18_best.pt"
OUT_CSV    = f"/Users/yhu10/Desktop/VLM/pipline_data_patch_level/runs/patch_clf/{SLIDE_ID}_pred.csv"
PATCH_SIZE = 256

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
T = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.7,0.7,0.7], std=[0.2,0.2,0.2]),
])

def load_model():
    m = models.resnet18(weights=None)
    m.fc = nn.Linear(m.fc.in_features, 2)
    m.load_state_dict(torch.load(CKPT, map_location=device))
    m.eval().to(device)
    return m

def main():
    slide = openslide.OpenSlide(SLIDE_PATH)
    with h5py.File(H5_PATH, "r") as f:
        coords = f["coords"][:]  # (N,2)

    model = load_model()
    probs = []
    bs = 64
    for i in range(0, len(coords), bs):
        batch = coords[i:i+bs]
        imgs = []
        for (x,y) in batch:
            img = slide.read_region((int(x),int(y)), 0, (PATCH_SIZE, PATCH_SIZE)).convert("RGB")
            imgs.append(T(img))
        imgs = torch.stack(imgs).to(device)
        with torch.no_grad():
            logits = model(imgs)
            p = torch.softmax(logits, dim=1)[:,1]  # prob of tumor class
        probs.extend(p.cpu().numpy().tolist())

    df = pd.DataFrame({"x": coords[:,0].astype(int), "y": coords[:,1].astype(int), "prob_tumor": probs})
    df.to_csv(OUT_CSV, index=False)

    # 简单的 slide-level 汇总（你可换其它规则）
    mean_prob = float(np.mean(probs))
    frac_high = float(np.mean((np.array(probs) >= 0.5)))
    slide_pred = "tumor" if mean_prob >= 0.5 else "benign"
    meta = {"slide_id": SLIDE_ID, "mean_prob": mean_prob, "frac_prob_ge_0.5": frac_high, "slide_pred": slide_pred}
    with open(Path(OUT_CSV).with_suffix(".json"), "w") as f:
        json.dump(meta, f, indent=2)
    print("Saved:", OUT_CSV)
    print("Slide-level:", meta)

if __name__ == "__main__":
    main()
