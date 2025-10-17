import os, json, random
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import openslide
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms

# ------------ Config (改这些路径/名字即可) ------------
SLIDE_ID = "CMU-2"
SLIDE_PATH = f"/Users/yhu10/Desktop/VLM/pipline_data_patch_level/data/slides/{SLIDE_ID}.svs"
LABEL_CSV = f"/Users/yhu10/Desktop/VLM/pipline_data_patch_level/data/labels/{SLIDE_ID}_patch_labels.csv"
OUT_DIR   = "/Users/yhu10/Desktop/VLM/pipline_data_patch_level/runs/patch_clf"
PATCH_SIZE = 256
BATCH_SIZE = 32
EPOCHS = 10  # 只有48个样本，10个epoch就够；如果你再标注多些再加
LR = 1e-4
VAL_SPLIT = 0.2
SEED = 42
# ------------------------------------------------------

os.makedirs(OUT_DIR, exist_ok=True)
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)

class SlidePatchDataset(Dataset):
    def __init__(self, slide_path, df, aug=False):
        self.slide = openslide.OpenSlide(slide_path)
        self.df = df.reset_index(drop=True)
        self.aug = aug
        self.T = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.7,0.7,0.7], std=[0.2,0.2,0.2]),
        ])
        self.T_aug = transforms.Compose([
            transforms.ToTensor(),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(0.1,0.1,0.1,0.05),
            transforms.Normalize(mean=[0.7,0.7,0.7], std=[0.2,0.2,0.2]),
        ])
        self.class_to_idx = {"benign":0, "tumor":1}

    def __len__(self):
        return len(self.df)

    def __getitem__(self, i):
        r = self.df.iloc[i]
        x, y = int(r.x), int(r.y)
        img = self.slide.read_region((x, y), 0, (PATCH_SIZE, PATCH_SIZE)).convert("RGB")
        img = self.T_aug(img) if self.aug else self.T(img)
        ylab = self.class_to_idx[r.label]
        return img, torch.tensor(ylab, dtype=torch.long)

def split_df(df, val_split=0.2):
    idx = np.arange(len(df))
    np.random.shuffle(idx)
    n_val = max(1, int(len(df)*val_split))
    val_idx = idx[:n_val]
    tr_idx  = idx[n_val:]
    return df.iloc[tr_idx].copy(), df.iloc[val_idx].copy()

def make_model():
    m = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    m.fc = nn.Linear(m.fc.in_features, 2)
    return m

def main():
    df = pd.read_csv(LABEL_CSV)
    # 处理极度类不平衡：计算权重
    vc = df["label"].value_counts().to_dict()
    n_benign = vc.get("benign",0); n_tumor = vc.get("tumor",0)
    class_weights = torch.tensor([1.0, 1.0], dtype=torch.float32)
    if n_benign>0 and n_tumor>0:
        # 简单反比
        total = n_benign + n_tumor
        w_b = total/(2*n_benign); w_t = total/(2*n_tumor)
        class_weights = torch.tensor([w_b, w_t], dtype=torch.float32)
    print("class counts:", vc, "class_weights:", class_weights.tolist())

    train_df, val_df = split_df(df, VAL_SPLIT)
    train_ds = SlidePatchDataset(SLIDE_PATH, train_df, aug=True)
    val_ds   = SlidePatchDataset(SLIDE_PATH, val_df, aug=False)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader   = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = make_model().to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights.to(device))
    optimizer = optim.AdamW(model.parameters(), lr=LR)

    best_val = 0.0
    for epoch in range(1, EPOCHS+1):
        model.train()
        tr_loss = tr_correct = tr_total = 0
        for imgs, labs in train_loader:
            imgs, labs = imgs.to(device), labs.to(device)
            optimizer.zero_grad()
            logits = model(imgs)
            loss = criterion(logits, labs)
            loss.backward()
            optimizer.step()
            tr_loss += loss.item()*imgs.size(0)
            tr_correct += (logits.argmax(1)==labs).sum().item()
            tr_total += imgs.size(0)
        tr_acc = tr_correct / max(1,tr_total)

        model.eval()
        va_loss = va_correct = va_total = 0
        with torch.no_grad():
            for imgs, labs in val_loader:
                imgs, labs = imgs.to(device), labs.to(device)
                logits = model(imgs)
                loss = criterion(logits, labs)
                va_loss += loss.item()*imgs.size(0)
                va_correct += (logits.argmax(1)==labs).sum().item()
                va_total += imgs.size(0)
        va_acc = va_correct / max(1,va_total)
        print(f"Epoch {epoch:02d} | train_acc {tr_acc:.3f} | val_acc {va_acc:.3f}")

        if va_acc >= best_val:
            best_val = va_acc
            torch.save(model.state_dict(), f"{OUT_DIR}/resnet18_best.pt")
    # 也保存最后一版
    torch.save(model.state_dict(), f"{OUT_DIR}/resnet18_last.pt")
    with open(f"{OUT_DIR}/meta.json","w") as f:
        json.dump({"slide_id":SLIDE_ID,"patch_size":PATCH_SIZE,"counts":vc,"best_val_acc":best_val}, f, indent=2)

if __name__ == "__main__":
    main()
