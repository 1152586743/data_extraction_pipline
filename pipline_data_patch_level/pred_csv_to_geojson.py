import json, pandas as pd
from pathlib import Path

SLIDE_ID = "CMU-2"
PRED_CSV = f"/Users/yhu10/Desktop/VLM/pipline_data_patch_level/runs/patch_clf/{SLIDE_ID}_pred.csv"
OUT_GEO  = f"/Users/yhu10/Desktop/VLM/pipline_data_patch_level/runs/patch_clf/{SLIDE_ID}_pred.geojson"

df = pd.read_csv(PRED_CSV)   # 需要列: x, y, prob_tumor

features = []
for r in df.itertuples():
    features.append({
        "type": "Feature",
        "id": f"patch_{r.Index}",
        "geometry": {
            "type": "Point",
            "coordinates": [float(r.x), float(r.y)]
        },
        "properties": {
            # 不要放 classification，避免 PathClass 解析错误
            "isLocked": False,
            # 关键：QuPath 0.6 要求 measurements 是 “数组” 结构
            "measurements": [
                {"name": "prob_tumor", "value": float(r.prob_tumor)}
            ]
        }
    })

geo = {"type": "FeatureCollection", "features": features}
Path(OUT_GEO).parent.mkdir(parents=True, exist_ok=True)
with open(OUT_GEO, "w") as f:
    json.dump(geo, f)
print("Saved:", OUT_GEO)
